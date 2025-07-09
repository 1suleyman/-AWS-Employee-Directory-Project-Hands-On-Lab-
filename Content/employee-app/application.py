# /employee-app/application.py

import os
import uuid
import boto3
import requests
from flask import Flask, request, render_template, redirect, url_for
from multiprocessing import Process
import time

# Initialize Flask app
application = Flask(__name__)

# --- AWS Configuration ---
# Read environment variables set in the EC2 User Data
PHOTOS_BUCKET = os.environ.get('PHOTOS_BUCKET')
AWS_REGION = os.environ.get('AWS_DEFAULT_REGION')
DYNAMO_MODE_ON = os.environ.get('DYNAMO_MODE') == 'on'
DYNAMO_TABLE_NAME = 'Employees'

# Initialize Boto3 clients if services are enabled
s3_client = None
dynamodb_resource = None
if PHOTOS_BUCKET:
    s3_client = boto3.client('s3', region_name=AWS_REGION)

if DYNAMO_MODE_ON:
    dynamodb_resource = boto3.resource('dynamodb', region_name=AWS_REGION)
    employees_table = dynamodb_resource.Table(DYNAMO_TABLE_NAME)

# --- Helper Functions ---
def get_instance_metadata(path):
    """Fetches specific EC2 instance metadata."""
    try:
        response = requests.get(f'http://169.254.169.254/latest/meta-data/{path}', timeout=2)
        return response.text
    except requests.exceptions.RequestException:
        return f"Not an EC2 instance or metadata service unavailable."

def cpu_stress(duration_s):
    """A simple function to stress the CPU."""
    end_time = time.time() + duration_s
    while time.time() < end_time:
        pass # Burn CPU cycles

# --- Flask Routes ---
@application.route('/')
def index():
    """Renders the main page with a list of employees."""
    employees = []
    if DYNAMO_MODE_ON:
        try:
            response = employees_table.scan()
            # Generate presigned URLs for each employee photo
            for item in response.get('Items', []):
                if 'objectKey' in item and s3_client:
                    item['photo_url'] = s3_client.generate_presigned_url(
                        'get_object',
                        Params={'Bucket': PHOTOS_BUCKET, 'Key': item['objectKey']},
                        ExpiresIn=3600  # URL valid for 1 hour
                    )
            employees = sorted(response.get('Items', []), key=lambda x: x.get('name', ''))
        except Exception as e:
            print(f"Error scanning DynamoDB table: {e}")
            # Handle case where table doesn't exist yet
            pass

    return render_template('index.html', employees=employees, bucket_name=PHOTOS_BUCKET)

@application.route('/add', methods=['POST'])
def add_employee():
    """Handles adding a new employee."""
    if not DYNAMO_MODE_ON or not s3_client:
        return "Database or S3 not enabled.", 400

    employee_id = str(uuid.uuid4())
    name = request.form.get('name')
    title = request.form.get('title')
    location = request.form.get('location')
    badges = request.form.get('badges')
    photo = request.files.get('photo')

    db_item = {
        'id': employee_id,
        'name': name,
        'title': title,
        'location': location,
        'badges': badges
    }

    # Handle photo upload to S3
    if photo and photo.filename != '':
        object_key = f"photos/{employee_id}-{photo.filename}"
        s3_client.upload_fileobj(
            photo,
            PHOTOS_BUCKET,
            object_key
        )
        db_item['objectKey'] = object_key

    # Save metadata to DynamoDB
    employees_table.put_item(Item=db_item)

    return redirect(url_for('index'))

@application.route('/info')
def info():
    """Displays instance metadata for load balancer testing."""
    instance_id = get_instance_metadata('instance-id')
    availability_zone = get_instance_metadata('placement/availability-zone')
    return f"<h1>Instance Info</h1><p><b>Instance ID:</b> {instance_id}</p><p><b>Availability Zone:</b> {availability_zone}</p>"

@application.route('/stress-cpu')
def stress():
    """Initiates a CPU stress test to trigger Auto Scaling."""
    duration = int(request.args.get('duration', 60)) # Default 60 seconds
    p = Process(target=cpu_stress, args=(duration,))
    p.start()
    return f"CPU stress test started for {duration} seconds."

if __name__ == '__main__':
    application.run(host='0.0.0.0', port=80, debug=True)
