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

### 🌐 Module 3: Networking (Coming Soon)
- Introduction to Networking
- Amazon VPC
- VPC Routing
- VPC Security (Security Groups, NACLs)
- Demonstration: Relaunching the App in EC2 with VPC settings

---

### 💾 Module 4: Storage (Coming Soon)
- File Storage (EFS, FSx)
- Block Storage (EBS, Instance Store)
- Object Storage (S3)
- Choosing the Right Storage
- Demonstration: Creating an Amazon S3 Bucket

---

### 🗄️ Module 5: Databases (Coming Soon)
- Introduction to AWS Databases
- Amazon RDS
- Purpose-Built Databases
- Amazon DynamoDB
- Choosing the Right Database
- Demonstration: Implementing Amazon DynamoDB

---

### 📈 Module 6: Monitoring & Optimization (Coming Soon)
- Amazon CloudWatch
- Traffic Routing with Elastic Load Balancing
- EC2 Auto Scaling
- Solution Optimization
- Demonstration: Making the App Highly Available
- Redesigning the Application Architecture
