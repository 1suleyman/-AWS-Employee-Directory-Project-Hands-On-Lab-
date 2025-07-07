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

### 🚀 Module 2: Hosting the Application on EC2 (Coming Soon)

#### 🔜 Up Next:
- Getting Started with Amazon EC2
- Amazon EC2 Instance Lifecycle
- Demonstration: Launching the Employee Directory Application on Amazon EC2

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
