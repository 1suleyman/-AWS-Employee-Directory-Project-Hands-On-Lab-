# -AWS-Employee-Directory-Project-Hands-On-Lab-

Welcome! This repository documents my hands-on journey through building a **serverless employee directory web application** on AWS. The goal is to apply cloud infrastructure skills by building a real project step-by-step, aligned with AWS best practices.

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

### 🔐 Module 1: Identity and Access Management (Complete)

#### ✅ Topics Covered:
- Protecting the AWS Root User
- AWS Identity and Access Management
- IAM Policies, Groups, Users
- IAM Roles for EC2
- Access Key Management
- Demonstration: Implementing Security with IAM

#### 🧱 Tasks Completed:
- [x] Enabled MFA for Root User
- [x] Created Admin IAM User & Group (`EC2Admins`)
- [x] Attached `AmazonEC2FullAccess` to Group
- [x] Created `EmployeeWebAppRole` for EC2 with:
  - `AmazonS3FullAccess`
  - `AmazonDynamoDBFullAccess`
- [x] Created IAM user for CLI with programmatic access keys
- [x] Deleted access key after demonstration

---

### 🚀 Module 2: Hosting the Application on EC2 (In Progress)

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

### 💾 Module 4: Storage
- File Storage (EFS, FSx)
- Block Storage (EBS, Instance Store)
- Object Storage (S3)
- Choosing the Right Storage
- Demonstration: Creating an Amazon S3 Bucket

---

### 🗄️ Module 5: Databases
- Introduction to AWS Databases
- Amazon RDS
- Purpose-Built Databases
- Amazon DynamoDB
- Choosing the Right Database
- Demonstration: Implementing Amazon DynamoDB

---

### 📈 Module 6: Monitoring & Optimization
- Amazon CloudWatch
- Traffic Routing with Elastic Load Balancing
- EC2 Auto Scaling
- Solution Optimization
- Demonstration: Making the App Highly Available
- Redesigning the Application Architecture
