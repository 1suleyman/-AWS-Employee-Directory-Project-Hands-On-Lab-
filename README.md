# 🧑‍💻 AWS 3-Tier Employee Directory Web Application

Welcome to my personal AWS lab project! This repository documents my step-by-step journey building a **3-Tier Employee Directory Web Application** on AWS using cloud architecture best practices.

---

## 📌 Project Overview

The goal of this project was to gain hands-on experience designing, deploying, and scaling a production-style web application using core AWS services.

> 🎯 **Objective**: Build a secure, scalable, and highly available Employee Directory web application in the AWS Cloud.

This application is built using:

- **Amazon EC2** for compute (Flask web server)
- **Amazon S3** for storing employee profile photos
- **Amazon DynamoDB** for storing employee data
- **IAM** for secure user access and instance roles
- **Amazon VPC** for custom networking and subnet design
- **Elastic Load Balancer** for distributing web traffic across AZs
- **EC2 Auto Scaling** for dynamic instance management
- **[Planned] API Gateway + AWS Lambda** for a future serverless contact form feature

---

## 🗂️ Project Documentation

Quick links to the main learning artifacts in this repo:

- 📘 [Planned Steps](Content/planned.md) – Module-by-module breakdowns, setup plans, and architecture decisions.
- 🛠️ [Executed Walkthrough](Content/executed.md) – Hands-on implementation logs, screenshots, validations, and testing notes.

---

## 📊 Architecture Diagram

![Screenshot 2025-07-08 at 10 41 47](https://github.com/user-attachments/assets/0e6db769-0053-41a3-a6cf-d135515adbff)


---

## 🧠 What I Learned

This repo documents my end-to-end AWS project where I deployed a real-world, scalable web application using core cloud services. It covers networking, security, storage, compute, and automation — built step by step using best practices.

Here’s what I practiced and learned:

---

### ✅ Identity & Access Management (IAM)
- Enabled MFA on the root user for account protection  
- Created IAM users (`AdminUser`, `DevUser`) with console and programmatic access  
- Assigned least-privilege roles and attached managed policies via IAM groups  
- Created and attached IAM Roles (e.g. `EmployeeWebAppRole`) to EC2 for secure access to S3 and DynamoDB  
- Learned how IAM Identity Center defaults to `us-east-1` as a global service region

---

### ✅ Compute (Amazon EC2)
- Launched EC2 instances using Amazon Linux 2023 and Free Tier instance types  
- Attached IAM roles, security groups, and configured launch scripts (User Data)  
- Used browser-based EC2 Connect instead of SSH keys for secure access  
- Debugged failed EC2 app launches by checking `/var/log/cloud-init-output.log`  
- Used User Data scripts to install dependencies, run Flask, and serve static sites  

---

### ✅ Networking (Amazon VPC)
- Created a custom VPC (`app-vpc`) with a CIDR block of `10.1.0.0/16`  
- Created public and private subnets across multiple Availability Zones (AZs) for high availability  
- Attached an Internet Gateway and associated a route table for public internet access  
- Verified proper routing setup and subnet association for internet-facing workloads  

---

### ✅ Storage (Amazon S3)
- Created a private S3 bucket (`employee-photo-bucket-456s`) for photo uploads  
- Uploaded and tested access to image objects  
- Wrote and applied a secure bucket policy allowing only EC2 access via IAM role  
- Validated file uploads using both the app and the S3 console  

---

### ✅ Database (Amazon DynamoDB)
- Created a `Employees` table with partition key `id`  
- Connected the app to DynamoDB using environment variables  
- Tested full-stack integration: photo uploaded to S3, employee data stored in DynamoDB  
- Confirmed write success via app UI and direct console queries  

---

### ✅ Monitoring & Auto Scaling
- Set up an **Application Load Balancer (ALB)** across two AZs  
- Created a **Launch Template** and **Auto Scaling Group (ASG)** for the app  
- Configured health checks and target groups  
- Implemented target-tracking scaling based on CPU utilization  
- Simulated high CPU load using `/stress-cpu` to trigger automatic scaling  
- Verified that new instances launched and registered automatically under the ALB

---

This project taught me how to design, build, troubleshoot, and scale a full-stack cloud application on AWS. Every decision — from IAM to load balancing — reinforced key concepts used by real cloud engineers and tested in the AWS Certified Cloud Practitioner and Solutions Architect exams.

It’s more than just a demo — it’s **proof of hands-on, production-ready skills**.

## 📮 Feedback

Have ideas, questions, or want to collaborate on cloud projects?
Feel free to reach out or create an issue in the repo!

