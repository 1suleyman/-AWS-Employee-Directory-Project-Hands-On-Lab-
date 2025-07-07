# -AWS-Employee-Directory-Project-Hands-On-Lab-

Welcome! This repository documents my hands-on journey through building a **serverless employee directory web application** on AWS. The goal is to apply cloud infrastructure skills by building a real project step-by-step, aligned with AWS best practices.

![Screenshot 2025-07-04 at 17 11 16](https://github.com/user-attachments/assets/e31de371-4cf1-4980-856a-9eb1243f0d01)


---

## 📌 Project Goal

Create a secure, scalable employee directory app hosted on AWS using services like:
- IAM
- EC2
- S3
- DynamoDB
- CloudWatch
- Elastic Load Balancing
- Auto Scaling
- API Gateway & Lambda (in later modules)

---

## ✅ Module Checklist

Each module focuses on a core AWS concept and includes a step-by-step implementation guide I can follow when building the project independently.

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

Here’s your `README.md` section for **🗄️ Module 5: Databases – Implementing Amazon DynamoDB**, written in the same structured, checklist-style format to match your project’s previous modules:

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

> 🎉 The app is now fully functional with persistent data stored across Amazon S3 and DynamoDB!

---

### 📈 Module 6: Monitoring & Optimization (Coming Soon)
- Amazon CloudWatch
- Traffic Routing with Elastic Load Balancing
- EC2 Auto Scaling
- Solution Optimization
- Demonstration: Making the App Highly Available
- Redesigning the Application Architecture
