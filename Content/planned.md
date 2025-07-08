# Project Plan: AWS 3-Tier Employee Directory Application

This file outlines the **step-by-step implementation plan** I followed to build a production-style 3-Tier web application on AWS.

Each module in this guide focuses on a **core AWS concept** — including IAM, EC2, S3, VPC networking, DynamoDB, load balancing, and auto scaling — with clear instructions for how to set up each part independently.

📌 **Purpose:**  
To design, plan, and practice building cloud-native infrastructure from scratch — the *right* way — using AWS best practices.

📄 **Want to see it in action?**  
→ [Check out the executed steps with screenshots, configs, and validations »](./executed.md)

---

## 🗂️ Module Overview

The project is divided into 6 guided modules:

1. **IAM** — Set up secure access using users, groups, roles, and MFA  
2. **EC2** — Launch the application on a virtual server  
3. **VPC** — Design custom networking with public/private subnets  
4. **S3** — Store employee profile images with restricted access  
5. **DynamoDB** — Persist employee data using a NoSQL database  
6. **Monitoring & Scaling** — Add load balancing and auto scaling for high availability

---

Use this file as a **build checklist**. Once you’re ready to see how it played out in real life, jump over to [executed.md](./executed.md).

---

### 🚀 Module 1: Hosting the Employee Directory Application on AWS

#### 🔧 IAM Setup
- [ ] Enable **MFA for the AWS root user**
- [ ] Create IAM **admin user** (e.g. `AdminUser`)
- [ ] Create IAM **group** (e.g. `EC2Admins`)
- [ ] Attach `AmazonEC2FullAccess` policy to the group
- [ ] Add `AdminUser` to the group

#### 🧭 IAM Roles
- [ ] Create IAM **role** (`EmployeeWebAppRole`)
- [ ] Trusted entity type: `EC2`
- [ ] Attach managed policies:
  - [ ] `AmazonS3FullAccess`
  - [ ] `AmazonDynamoDBFullAccess`
- [ ] Review trust relationship: allow only EC2 to assume role

#### 🔑 IAM Users & Access Keys
- [ ] Create **developer IAM user** (e.g. `DevUser`)
- [ ] Enable console access and force password reset
- [ ] Add user to `EC2Admins` group
- [ ] Create programmatic access keys for AWS CLI use
- [ ] ✅ Delete keys after testing (demo only)

---

### 🚀 Module 2: Hosting the Application on EC2

#### 🖥️ EC2 Setup – Launch and Configure the Instance

- [ ] Navigate to EC2 Dashboard → **Launch Instance**
- [ ] Name instance: `employee-directory-app`
- [ ] Select AMI: `Amazon Linux 2023`
- [ ] Instance type: `t2.micro` (Free Tier)

#### 🔐 Key Pair
- [ ] Select: **Proceed without a key pair**
  - (Use EC2 browser-based Connect instead of SSH)

#### 🌐 Network Settings
- [ ] Use **default VPC** and **default subnet**
- [ ] Auto-assign Public IP: **Enabled**

#### 🔥 Security Group
- [ ] Remove SSH (port 22)
- [ ] Allow **HTTP (80)** – for web traffic
- [ ] Allow **HTTPS (443)** – optional future support

#### 📦 Storage
- [ ] Leave default root volume
- [ ] No additional EBS volumes

#### 🪪 IAM Instance Profile
- [ ] Attach IAM role: `EmployeeWebAppRole`
  - Grants EC2 instance access to S3 and DynamoDB

#### 📝 User Data (Launch Script)
```bash
#!/bin/bash
cd /home/ec2-user
wget https://<YOUR_BUCKET>.s3.amazonaws.com/employee-app.zip
unzip employee-app.zip
cd employee-app
yum install python3 -y
pip3 install -r requirements.txt
yum install stress -y
export PHOTOS_BUCKET=<your-bucket-name>
export AWS_DEFAULT_REGION=us-west-2
export DYNAMO_MODE=on
python3 application.py
```
> Replace your-bucket-name with your actual bucket

#### ✅ Post-Launch
- [ ] Wait for Instance Status Checks to pass
- [ ] Access the app via the EC2 public IP address
- [ ] Confirm the Employee Directory loads (empty state)

---

### 🌐 Module 3: Networking – Custom VPC Setup and Application Relaunch


#### 🛠️ VPC Setup
- [x] Created custom VPC: `app-vpc`
  - CIDR block: `10.1.0.0/16`

#### 🧱 Subnet Configuration
- [x] Created four subnets with non-overlapping ranges:
  - `Public Subnet 1` → `10.1.1.0/24` (AZ: `e.g. us-west-2a`)
  - `Private Subnet 1` → `10.1.2.0/24` (AZ: `e.g. us-west-2a`)
  - `Public Subnet 2` → `10.1.3.0/24` (AZ: `e.g. us-west-2b`)
  - `Private Subnet 2` → `10.1.4.0/24` (AZ: `e.g. us-west-2b`)

#### 🌐 Internet Gateway
- [x] Created and attached Internet Gateway: `app-igw`
  - Attached to `app-vpc`

#### 🧭 Public Route Table
- [x] Created route table: `public-route-table`
  - Destination: `0.0.0.0/0` → Target: Internet Gateway
  - Associated with:
    - `Public Subnet 1`
    - `Public Subnet 2`

> ✅ Reminder: Subnets are only considered "public" if they are associated with a route table that connects them to an Internet Gateway.

### 🔁 Relaunching the Employee Directory App in New VPC

#### 🔄 EC2 Re-deployment Steps
- [x] Navigated to EC2 → Selected existing instance → Actions → **Launch more like this**
- [x] Updated name: `Employee Directory App 2`
- [x] Selected:
  - AMI: Amazon Linux 2
  - Instance type: `t2.micro`
  - Proceed without key pair
- [x] Selected **new VPC**: `app-vpc`
- [x] Subnet: `Public Subnet 1`
- [x] Enabled Auto-assign Public IP

#### 🔒 Security Group (new)
- [x] Created new security group for `app-vpc`
  - Inbound rules:
    - HTTP (port 80) from anywhere
    - HTTPS (port 443) from anywhere

#### 🔐 IAM Role
- [x] Verified IAM role `EmployeeWebAppRole` was prepopulated in launch wizard

#### 🧾 User Data (prepopulated)
- [x] Confirmed launch script includes:
  - S3 download
  - Python/Flask installation
  - DynamoDB/S3 setup
  - Running on port 80

#### ✅ Validation
- [x] Waited for EC2 instance checks to pass
- [x] Accessed application via public IP
  - ✅ Employee Directory loaded successfully inside custom VPC

---

### 💾 Module 4: Storage – Creating & Connecting Amazon S3

This module provisions Amazon S3 to store employee profile photos, set secure access via IAM policies, and update the EC2-hosted application to utilize the bucket.

#### 🪣 S3 Bucket Creation & Object Upload
- [x] Created S3 bucket: `employee-photo-bucket-sr963`
  - Region: `us-west-2` (same as rest of app)
  - Default settings retained (no public access)
- [x] Uploaded test image to validate bucket
  - Used GUI Upload → `employee2.jpg`
  - Verified success in S3 console

#### 🔐 Bucket Policy Configuration
- [x] Navigated to **Permissions** tab → Edited **Bucket Policy**
- [x] Customized IAM policy:
  - Replaced `INSERT-ACCOUNT-NUMBER` with actual account number
  - Replaced `INSERT-BUCKET-NAME` with actual bucket name
  - Removed `<>` brackets
- [x] Saved policy to allow access from EC2 via IAM Role (`EmployeeWebAppRole`)

#### 🔁 EC2 Relaunch: App Configured to Use S3
- [x] Cloned existing EC2 instance
  - Used **Launch more like this** on stopped instance
  - Renamed to: `employee-directory-app-s3`
- [x] Verified:
  - Same AMI and instance type (`t2.micro`)
  - Auto-assign Public IP → **Enabled**
  - IAM Role pre-populated: `EmployeeWebAppRole`

#### ⚙️ User Data Configuration
- [x] Updated EC2 user data with S3 bucket name
  - Set environment variable: `PHOTOS_BUCKET=employee-photo-bucket-sr963`
  - Launch script pulls app files from S3 and installs dependencies

#### ✅ Validation
- [x] Waited for EC2 status checks → **2/2 checks passed**
- [x] Opened public IP in browser
  - ✅ Application launched successfully with S3 bucket integration
  - ❗ Note: Database (DynamoDB) not yet configured for interaction

#### 🧹 Cleanup
- [x] Stopped demo instance (optional for cost saving)
- [x] Deleted uploaded S3 object (test image)

---

### 🗄️ Module 5: Databases – Implementing Amazon DynamoDB

This module connects the Employee Directory app to a backend database using Amazon DynamoDB, enabling persistent data storage and full CRUD capability.

#### 🧪 EC2 Relaunch for Database Integration
- [x] Cloned most recent S3-enabled EC2 instance:
  - Used **Launch more like this** on `employee-directory-app-s3`
  - Renamed to: `employee-directory-app-dynamodb`
- [x] Verified key settings:
  - ✅ IAM Role: `EmployeeWebAppRole`
  - ✅ Auto-assign Public IP: Enabled
  - ✅ User data script includes correct S3 bucket name
- [x] Launched instance and waited for **2/2 status checks**

#### 🧭 Amazon DynamoDB Table Setup
- [x] Navigated to **DynamoDB** console → Clicked **Create Table**
- [x] Table name: `Employees`
- [x] Partition key: `id` (String)
- [x] Used all default settings → Clicked **Create Table**

#### ✅ Application Test: End-to-End Integration
- [x] Opened new EC2 public IP in browser
- [x] Verified application was running
- [x] Added employee entry via UI form:
  - ✅ Name, Location, Job Title, Badges, and Photo
  - ✅ Clicked **Save** and confirmed employee added to directory

#### 📂 Verification: Data Stored in S3 and DynamoDB
- [x] Opened S3 Bucket → Confirmed new object (photo) uploaded
- [x] Opened DynamoDB Table → Explored items
  - ✅ Entry with employee info
  - ✅ Correct `id`, `name`, `badges`, and `objectKey` fields present

#### 🧹 Cleanup
- [x] Stopped `employee-directory-app-dynamodb` EC2 instance to avoid charges
- [ ] DynamoDB Table left running (ready for next module)

---

### 📈 Module 6: Monitoring & Optimization – Load Balancing & Auto Scaling

In this last module, the Employee Directory application is scaled for high availability and fault tolerance using an Application Load Balancer and EC2 Auto Scaling Group.

#### 🚀 EC2 Relaunch for Load Balancing Setup
- [x] Cloned latest app instance: `employee-directory-app-dynamodb`
- [x] Renamed new instance: `employee-directory-app-lb`
- [x] Verified:
  - ✅ Public IP: Enabled
  - ✅ IAM Role: `EmployeeWebAppRole`
  - ✅ User data: Correct S3 bucket + region
- [x] Launched instance & confirmed 2/2 health checks
- [x] Tested app endpoint manually to confirm it's functional

#### 🌐 Application Load Balancer Setup
- [x] Navigated to EC2 → Load Balancers → **Create Application Load Balancer**
- [x] Name: `app-elb`
- [x] Configuration:
  - ✅ Internet-facing
  - ✅ VPC: `app-vpc`
  - ✅ Availability Zones: `us-west-2a`, `us-west-2b`
- [x] Created Security Group: `load-balancer-sg`
  - ✅ Inbound: Allow HTTP (port 80) from anywhere
- [x] Listener:
  - ✅ Target group type: **Instance**
  - ✅ Target group name: `app-target-group`
  - ✅ Health checks configured:
    - Protocol: HTTP
    - Path: `/`
    - Thresholds: Healthy = 2, Unhealthy = 5
    - Timeout: 30s, Interval: 40s
- [x] Registered target: `employee-directory-app-lb` instance
- [x] Load balancer became **Active**
- [x] Copied DNS endpoint → Confirmed application accessible via ALB

#### 📄 Launch Template for Auto Scaling
- [x] Created Launch Template: `app-launch-template`
  - ✅ Instance type: `t2.micro` (Free Tier)
  - ✅ Network: `app-vpc` + Web SG
  - ✅ IAM Role: `EmployeeWebAppRole`
  - ✅ User data: Updated with correct bucket & region
- [x] Verified: Launch template ready for Auto Scaling group

#### 📈 Auto Scaling Group (ASG) Setup
- [x] Created ASG: `app-asg` using launch template
- [x] Configured:
  - ✅ VPC: `app-vpc`
  - ✅ Subnets: `Public Subnet 1` + `Public Subnet 2`
  - ✅ Load Balancer Target Group: `app-target-group`
  - ✅ Health Check Type: ELB
- [x] Set group size:
  - ✅ Desired: 2
  - ✅ Min: 2
  - ✅ Max: 4
- [x] Target tracking scaling policy:
  - ✅ Metric: Avg CPU utilization
  - ✅ Threshold: 60%
  - ✅ Warm-up: 300s

#### 🔁 Testing Auto Scaling
- [x] Appended `/info` to ALB DNS to verify instance routing
- [x] Used `/stress-cpu?duration=10m` to simulate load
- [x] Monitored Target Group health
- [x] ✅ Observed Auto Scaling: 2 new EC2 instances launched

> 🎯 Outcome: Application is now highly available and scalable with built-in fault tolerance and load distribution across multiple Availability Zones.
