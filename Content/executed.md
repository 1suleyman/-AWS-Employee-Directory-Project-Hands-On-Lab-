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

### 🔧 IAM Setup

#### Enable **MFA for the AWS root user**

![Screenshot 2025-07-08 at 11 32 58](https://github.com/user-attachments/assets/8bc278e4-5b3f-42da-804b-9aafab5bd768)

#### Create IAM **admin user** (e.g. `AdminUser`)

**🧠 Question: Should I Give Console Access to My AdminUser?**

![Screenshot 2025-07-08 at 12 13 16](https://github.com/user-attachments/assets/66d576de-97b5-4cb8-8edf-4ddc336f17ac)

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

## 🌍 Question: Why Is IAM Identity Center Defaulting to US East (N. Virginia)

![Screenshot 2025-07-08 at 12 32 43](https://github.com/user-attachments/assets/7a2c95e8-3b3d-47dd-95e6-e60c3f988b15)

After I selected:

> **"Are you providing console access to a person?"**  
> and saw the message:  
> _“We recommend that you use Identity Center to provide console access to a person...”_

![Screenshot 2025-07-08 at 12 39 34](https://github.com/user-attachments/assets/cda9637a-3ec0-411f-9ce5-2a5ec6dc8616)


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

## 🔐 Question: Should I Use an Autogenerated or Custom Password for the AdminUser?

![Screenshot 2025-07-08 at 14 26 53](https://github.com/user-attachments/assets/7efdb2c5-fee7-456c-8198-b9ed95e129ee)

When creating the `AdminUser`, I reached the **"Console password"** section, where AWS gives two options:

> **Autogenerated password**  
> You can view the password after you create the user.

> **Custom password**  
> You enter a password manually now (must be 8+ characters with at least 3 of: uppercase, lowercase, numbers, symbols)

There’s also a checkbox:  
> ✅ **Users must create a new password at next sign-in (Recommended)**

### 🧠 What I Considered

#### ✅ Autogenerated Password – Good if:
- You want **maximum randomness** and **strong security** by default
- You're okay with copying and saving the password temporarily
- You're **sharing the credentials** securely with someone else
- You **want the user to reset it anyway** at first login (via the recommended checkbox)

#### 🔓 Custom Password – Good if:
- You're the one using the account and want something easy to **remember temporarily**
- You're doing **short-term lab work** and don’t want to reset a password immediately
- You want to **avoid the "reset password on first login" step**

#### ✅ My Choice

Since I’m doing **solo hands-on work** and managing everything myself:

- I used a **custom password** that I could remember quickly
- I **unchecked** the “must reset password on next sign-in” box to avoid extra steps
- I made sure the password was strong enough to meet AWS requirements

> Later, when the lab is complete, I can always reset the password or rotate credentials

---
- [x] Create IAM **group** (e.g. `EC2Admins`)
---

![Screenshot 2025-07-08 at 14 28 50](https://github.com/user-attachments/assets/aa9762a6-2243-4cb9-8c46-b2a2923dca70)

---
- [x] Attach `AmazonEC2FullAccess` policy to the group
---

![Screenshot 2025-07-08 at 14 29 41](https://github.com/user-attachments/assets/36f1bb54-c0c7-405e-8bb5-b7feced2cd62)

---
- [x] Add `AdminUser` to the group
---

![Screenshot 2025-07-08 at 14 30 28](https://github.com/user-attachments/assets/28d4a7e9-6a68-43bc-81e1-f5e25264660b)

#### 🧭 IAM Roles
---
- [x] Create IAM **role** (`EmployeeWebAppRole`)
---

![Screenshot 2025-07-08 at 14 40 09](https://github.com/user-attachments/assets/63c43585-b0f8-4a84-904e-93b371bcfdfe)


---
- [x] Trusted entity type: `EC2`
---

![Screenshot 2025-07-08 at 14 37 35](https://github.com/user-attachments/assets/28a31b26-bbf6-4242-be17-f45342c7db53)

---
- [x] Attach managed policies:
  - [x] `AmazonS3FullAccess`
  - [x] `AmazonDynamoDBFullAccess`
---

![Screenshot 2025-07-08 at 14 38 37](https://github.com/user-attachments/assets/ee1acff5-0d8a-4664-8eb8-5f2eb68464a8)

![Screenshot 2025-07-08 at 14 39 17](https://github.com/user-attachments/assets/5a693511-5815-4f78-b2da-26497fe15665)

---
- [x] Review trust relationship: allow only EC2 to assume role
---

![Screenshot 2025-07-08 at 14 40 22](https://github.com/user-attachments/assets/a9f85236-caeb-409f-b14b-e67d1c3f98ca)


#### 🔑 IAM Users & Access Keys
---
- [ ] Create **developer IAM user** (e.g. `DevUser`)
---

![Screenshot 2025-07-08 at 14 43 41](https://github.com/user-attachments/assets/0b39df9a-f37e-4e10-b95e-7511b131f81f)

---
- [x] Enable console access and force password reset
---
![Screenshot 2025-07-08 at 14 45 03](https://github.com/user-attachments/assets/0faf2d76-0998-4614-ab71-bd5d37e60cb4)

![Screenshot 2025-07-08 at 14 46 12](https://github.com/user-attachments/assets/574d7119-97d5-41ec-a161-02c37bf9cf01)

Since I’m doing **solo hands-on work** and managing everything myself:

- I used a **custom password** that I could remember quickly
- I **unchecked** the “must reset password on next sign-in” box to avoid extra steps
- I made sure the password was strong enough to meet AWS requirements

---
- [x] Add user to `EC2Admins` group
---

![Screenshot 2025-07-08 at 14 46 57](https://github.com/user-attachments/assets/afcfe4e9-9ae1-403d-9dd9-802c89872691)

---
- [x] Create programmatic access keys for AWS CLI use
---

![Screenshot 2025-07-08 at 14 50 51](https://github.com/user-attachments/assets/44808af4-b070-4ae7-858b-ef4897f14cf2)

---
- [x] ✅ Delete keys after testing
---

![Screenshot 2025-07-08 at 14 53 32](https://github.com/user-attachments/assets/1708b704-811f-4d3d-8825-91b17017c795)

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
