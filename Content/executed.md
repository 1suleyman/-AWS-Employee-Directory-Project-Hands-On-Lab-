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
   
- [x] Create IAM **admin user** (e.g. `AdminUser`)

![Screenshot 2025-07-08 at 12 13 16](https://github.com/user-attachments/assets/66d576de-97b5-4cb8-8edf-4ddc336f17ac)

#### 🧠 Decision Point: Should I Give Console Access to My AdminUser?

Once I got to this stage — creating my IAM admin user — I paused to ask myself:

> **“Should I provide user access to the AWS Management Console or not?”**

This is an important decision depending on how I plan to interact with AWS.

#### 🤔 Should AdminUser Have Console Access?

#### ✅ YES – Enable Console Access if:

- I want to **manually deploy, troubleshoot, or inspect** services in the AWS UI.
- I’m following this **guided lab course**, which includes **demoing in the console**.
- I need to **reset passwords**, configure IAM users, VPCs, and other settings through the browser.
- I’m the **only person managing this AWS account**, so I need full UI access.

#### ❌ NO – Don’t Enable Console Access if:

- I’m using this IAM user purely for **automation or infrastructure-as-code** (e.g. CloudFormation, Bicep, Terraform).
- I have a **CI/CD pipeline or SDK-based script** doing the work instead of me.
- I want to **enforce least privilege** and avoid storing browser login credentials.

#### ⚖️ My Use Case (for This Project)

Since this is a **hands-on, manually driven project**, where I’m:

- Deploying and testing services like **EC2, IAM, S3, and DynamoDB**
- Using the **AWS Management Console**
- Learning step-by-step before moving into automation

#### ✅ My Choice

I chose to **enable AWS Management Console access** for the AdminUser.
This gives me the flexibility to:

- Log in and use the browser-based AWS UI
- Perform tasks manually as I follow the lab instructions

Later on, I can rotate to programmatic-only access when I start automating or building infrastructure as code.

![Screenshot 2025-07-08 at 12 32 43](https://github.com/user-attachments/assets/7a2c95e8-3b3d-47dd-95e6-e60c3f988b15)

## 🌍 Question: Why Is IAM Identity Center Defaulting to US East (N. Virginia)?

After I selected:

> **"Are you providing console access to a person?"**  
> and saw the message:  
> _“We recommend that you use Identity Center to provide console access to a person...”_

I continued to the **IAM Identity Center setup** under **AWS Organizations**, but something confused me:

> **Why is it defaulting to `US East (N. Virginia)` as the current AWS Region, even though I’m based in London?**

### 📌 What I Learned

- **IAM Identity Center (formerly AWS SSO)** is a **global service**, but it needs a **home Region** to store identity-related configurations.
- As of now, **`us-east-1` (N. Virginia)** is the only supported Region for setting up IAM Identity Center.
- This Region is **not changeable**, even if your main AWS infrastructure is located in another Region (like `eu-west-2` for London).
- The Identity Center setup and assignments are global — **but the backend data is stored in N. Virginia**.

### ⚙️ How It Affects This Project

- My **compute, storage, and database resources** are all in the London (`eu-west-2`) Region.
- IAM Identity Center being locked to `us-east-1` does **not block or conflict** with my project.
- I can still:
  - Assign users access to AWS accounts across any Region
  - Manage permissions for services like EC2, S3, and DynamoDB within my local Region

### ✅ Conclusion

Although it feels unintuitive, this is the current AWS design.  
I went ahead and used IAM Identity Center in `us-east-1`, knowing it won’t interfere with my London-based infrastructure.
   
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
