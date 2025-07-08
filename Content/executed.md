# Project Execution: AWS 3-Tier Employee Directory Application

Welcome to the hands-on execution log of my **AWS 3-Tier Employee Directory Web Application Project**.  
This file documents the **exact steps I took** — from IAM setup to Auto Scaling — to bring this application to life on AWS, module by module.

Think of this as a **behind-the-scenes build journal** that tracks not just what I planned to do — but what I actually did, validated, and learned.

---

## 🧠 What You’ll Find Here

✅ **Completed modules** with verified setups  
🖼️ **Screenshots and config details** of my AWS Console setup  
🧪 **Tests and validations** of the deployed infrastructure  
📦 **Cleanup and cost-saving practices** at every stage

Each section below matches the structure of my [planned project guide](./planned.md) — but this version focuses purely on implementation and results.

---

## 📋 Execution Modules

- **🚀 Module 1:** IAM Setup (Users, Groups, Roles, MFA, Access Keys)  
- **🚀 Module 2:** Launching the App on EC2 (Networking, User Data, Web Server)  
- **🌐 Module 3:** Custom VPC with Subnets, Route Tables, and Re-deployment  
- **💾 Module 4:** S3 Bucket for Profile Photos + IAM Policy Integration  
- **🗄️ Module 5:** DynamoDB Table Setup + Full CRUD Test via App UI  
- **📈 Module 6:** Load Balancing and EC2 Auto Scaling Configuration + Stress Test

Each module ends with real validation: "Did it work?" If so, ✅. If not, I tracked the fix.

---

## 🔍 Why Document Execution?

Writing this was part of my **learning-through-doing** approach. I didn’t just read about AWS — I built something, broke things, fixed them, and learned *why* each service mattered.

If you're building a similar app, studying for AWS certs, or want to understand how these services connect in practice, this log is for you.

---

## 🚀 Module 1: IAM Setup

#### 🔧 IAM Setup
- [x] Enable **MFA for the AWS root user**

![Screenshot 2025-07-08 at 11 32 58](https://github.com/user-attachments/assets/8bc278e4-5b3f-42da-804b-9aafab5bd768)
   
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
- [ ] ✅ Delete keys after testing 

---

## 🚀 Module 2: Launching the App on EC2

!-- Fill in EC2 launch steps, user data script, validation steps --
🧹 **Optional:** Finish each module with cleanup steps to avoid unexpected AWS charges!

---

## 🌐 Module 3: VPC Networking + Re-deploy

!-- Custom VPC, subnets, IGW, route tables, and app redeployment --
🧹 **Optional:** Finish each module with cleanup steps to avoid unexpected AWS charges!

---

## 💾 Module 4: Storage (S3 Integration)

!-- S3 bucket creation, bucket policy, EC2 app update, test upload --
🧹 **Optional:** Finish each module with cleanup steps to avoid unexpected AWS charges!

---

## 🗄️ Module 5: Database (DynamoDB Integration)

!-- DynamoDB table creation, full CRUD test via app --
🧹 **Optional:** Finish each module with cleanup steps to avoid unexpected AWS charges!

---

## 📈 Module 6: Monitoring & Auto Scaling

!-- Load balancer setup, ASG, launch template, stress test, scale-out --
🧹 **Optional:** Finish each module with cleanup steps to avoid unexpected AWS charges!
