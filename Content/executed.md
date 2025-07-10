
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

---

### 🔧 IAM Setup

---
- [x] Enable **MFA for the AWS root user**
---

![Screenshot 2025-07-08 at 11 32 58](https://github.com/user-attachments/assets/8bc278e4-5b3f-42da-804b-9aafab5bd768)

---
- [x] Create IAM **admin user** (e.g. `AdminUser`)
---

**🧠 Question: Should I Give Console Access to My AdminUser?**

![Screenshot 2025-07-08 at 12 13 16](https://github.com/user-attachments/assets/66d576de-97b5-4cb8-8edf-4ddc336f17ac)

Once I got to this stage — creating my IAM admin user — I paused to ask myself:

> **“Should I provide user access to the AWS Management Console or not?”**

This is an important decision depending on how I plan to interact with AWS.

**🤔 Should AdminUser Have Console Access?**

**✅ YES – Enable Console Access if:**

- I want to **manually deploy, troubleshoot, or inspect** services in the AWS UI.
- I’m following this **guided lab course**, which includes **demoing in the console**.
- I need to **reset passwords**, configure IAM users, VPCs, and other settings through the browser.
- I’m the **only person managing this AWS account**, so I need full UI access.

**❌ NO – Don’t Enable Console Access if:**

- I’m using this IAM user purely for **automation or infrastructure-as-code** (e.g. CloudFormation, Bicep, Terraform).
- I have a **CI/CD pipeline or SDK-based script** doing the work instead of me.
- I want to **enforce least privilege** and avoid storing browser login credentials.

**⚖️ My Use Case (for This Project)**

Since this is a **hands-on, manually driven project**, where I’m:

- Deploying and testing services like **EC2, IAM, S3, and DynamoDB**
- Using the **AWS Management Console**
- Learning step-by-step before moving into automation

**✅ My Choice**

I chose to **enable AWS Management Console access** for the AdminUser.
This gives me the flexibility to:

- Log in and use the browser-based AWS UI
- Perform tasks manually as I follow the lab instructions

Later on, I can rotate to programmatic-only access when I start automating or building infrastructure as code.

**🌍 Question: Why Is IAM Identity Center Defaulting to US East (N. Virginia)**

![Screenshot 2025-07-08 at 12 32 43](https://github.com/user-attachments/assets/7a2c95e8-3b3d-47dd-95e6-e60c3f988b15)

After I selected:

> **"Are you providing console access to a person?"**  
> and saw the message:  
> _“We recommend that you use Identity Center to provide console access to a person...”_

![Screenshot 2025-07-08 at 12 39 34](https://github.com/user-attachments/assets/cda9637a-3ec0-411f-9ce5-2a5ec6dc8616)

I continued to the **IAM Identity Center setup** under **AWS Organizations**, but something confused me:

> **Why is it defaulting to `US East (N. Virginia)` as the current AWS Region, even though I’m based in London?**

**📌 What I Learned**

- **IAM Identity Center (formerly AWS SSO)** is a **global service**, but it needs a **home Region** to store identity-related configurations.
- As of now, **`us-east-1` (N. Virginia)** is the only supported Region for setting up IAM Identity Center.
- This Region is **not changeable**, even if your main AWS infrastructure is located in another Region (like `eu-west-2` for London).
- The Identity Center setup and assignments are global — **but the backend data is stored in N. Virginia**.

**⚙️ How It Affects This Project**

- My **compute, storage, and database resources** are all in the London (`eu-west-2`) Region.
- IAM Identity Center being locked to `us-east-1` does **not block or conflict** with my project.
- I can still:
  - Assign users access to AWS accounts across any Region
  - Manage permissions for services like EC2, S3, and DynamoDB within my local Region

**✅ Conclusion**

Although it feels unintuitive, this is the current AWS design.  
I went ahead and used IAM Identity Center in `us-east-1`, knowing it won’t interfere with my London-based infrastructure.

**🔐 Question: Should I Use an Autogenerated or Custom Password for the AdminUser?**

When creating the `AdminUser`, I reached the **"Console password"** section, where AWS gives two options:

> **Autogenerated password**  
> You can view the password after you create the user.

> **Custom password**  
> You enter a password manually now (must be 8+ characters with at least 3 of: uppercase, lowercase, numbers, symbols)

There’s also a checkbox:  
> ✅ **Users must create a new password at next sign-in (Recommended)**

**🧠 What I Considered**

**✅ Autogenerated Password – Good if:**
- You want **maximum randomness** and **strong security** by default
- You're okay with copying and saving the password temporarily
- You're **sharing the credentials** securely with someone else
- You **want the user to reset it anyway** at first login (via the recommended checkbox)

**🔓 Custom Password – Good if:**
- You're the one using the account and want something easy to **remember temporarily**
- You're doing **short-term lab work** and don’t want to reset a password immediately
- You want to **avoid the "reset password on first login" step**

**✅ My Choice**

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

### 🧭 IAM Roles
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


### 🔑 IAM Users & Access Keys
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

#### 🖥️ EC2 Setup – Launch and Configure the Instance

---
- [x] Navigate to EC2 Dashboard → **Launch Instance**
---

![Screenshot 2025-07-08 at 15 48 13](https://github.com/user-attachments/assets/6e8ac15f-18aa-4496-8051-1feab401649b)

---
- [x] Name instance: `employee-directory-app`
---

![Screenshot 2025-07-08 at 15 48 47](https://github.com/user-attachments/assets/15626678-1227-4446-a2e6-8609687cd5a1)

---
- [x] Select AMI: `Amazon Linux 2023`
---

![Screenshot 2025-07-08 at 15 49 23](https://github.com/user-attachments/assets/aa0cd5e1-923e-4e37-9514-7bea38466798)

---
- [x] Instance type: `t2.micro` (Free Tier)
---

![Screenshot 2025-07-08 at 15 50 02](https://github.com/user-attachments/assets/52124ee1-64c7-48a4-9da9-803a15607295)

#### 🔐 Key Pair
---
- [x] Select: **Proceed without a key pair**
  - (As I'll be using EC2 browser-based Connect instead of SSH)
---

![Screenshot 2025-07-08 at 15 50 24](https://github.com/user-attachments/assets/a05c7ca9-89e4-40c7-8370-400027ebe2b8)

#### 🌐 Network Settings
---
- [x] Use **default VPC** and **default subnet**
---

![Screenshot 2025-07-08 at 15 51 38](https://github.com/user-attachments/assets/42a436de-570d-405a-aa3f-a671d2bef328)

---
- [x] Auto-assign Public IP: **Enabled**
---

![Screenshot 2025-07-08 at 15 52 05](https://github.com/user-attachments/assets/63543ec9-6f4f-46dd-8720-5b3bc0bc66ea)

#### 🔥 Security Group
---
- [x] Remove SSH (port 22)
---
---
- [x] Allow **HTTP (80)** – for web traffic
---

![Screenshot 2025-07-08 at 15 53 49](https://github.com/user-attachments/assets/780cdc39-e955-42b2-87c6-555514d63301)

---
- [x] Allow **HTTPS (443)** – optional future support
---

![Screenshot 2025-07-08 at 15 54 03](https://github.com/user-attachments/assets/8fad4e78-5525-490f-a413-a9943421402a)

#### 📦 Storage
---
- [x] Leave default root volume
---
---
- [x] No additional EBS volumes
---

#### 🪪 IAM Instance Profile
---
- [x] Attach IAM role: `EmployeeWebAppRole`
  - Grants EC2 instance access to S3 and DynamoDB
---

![Screenshot 2025-07-08 at 15 54 56](https://github.com/user-attachments/assets/d5583f68-77ff-43d5-b888-5436dc6896e7)

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
---
- [x] Wait for Instance Status Checks to pass
---

![Screenshot 2025-07-08 at 16 04 13](https://github.com/user-attachments/assets/f099ae1c-a31e-44bf-b999-15130b71aaec)

---
- [x] Access the app via the EC2 public IP address
---

**🧭 What Just Happened (My Summary)**

After launching my EC2 instance, I tried accessing the app using the public IP address — but I hit this error:

❌ This site can’t be reached
13.41.53.236 refused to connect
ERR_CONNECTION_REFUSED

That told me the app wasn’t running — most likely because the User Data launch script failed.

I checked /var/log/cloud-init-output.log and realized I never replaced this line in the script:

```bash
wget https://<YOUR_BUCKET>.s3.amazonaws.com/employee-app.zip
```

Because <YOUR_BUCKET> wasn’t updated with a real S3 bucket name, the EC2 instance failed to:

- Download the zip file
- Unzip the app
- Install the dependencies
- Start the Flask server

Basically, the app never launched — so there was nothing for the public IP to respond with.

**🔄 My Pivot: Serve a Static Website Instead**
Instead of chasing down a public bucket or recreating the Flask app zip file, I asked:

< “Can I just serve a basic HTML page from this EC2 instance instead?”

Turns out — **yes**. So I pivoted to testing my infrastructure setup by serving a static HTML page via Apache (httpd).

**✅ Working User Data Script (Static Site)**
```bash
#!/bin/bash
yum update -y
yum install -y httpd
systemctl start httpd
systemctl enable httpd

# Create a simple HTML page
cat <<EOF > /var/www/html/index.html
<!DOCTYPE html>
<html>
<head>
  <title>My First EC2 Website</title>
</head>
<body>
  <h1>🎉 Hello from EC2!</h1>
  <p>This static website was launched with a User Data script.</p>
</body>
</html>
EOF
```

**✅ EC2 Static Website Launched Successfully**

After correcting my User Data script and launching a fresh instance (`employee-directory-app-2`), I was able to:

- After launching a new instance (employee-directory-app-2) with the updated User Data, I was able to:
- Confirm httpd was installed and running: systemctl status httpd
- See that /var/www/html/index.html was created correctly
- Run curl http://localhost and curl http://<Public IP> — both returned the HTML
- Open the site in an Incognito browser window (fixed caching issues from earlier attempts)
- See the site load with a "Not Secure" message (expected with HTTP on port 80

🎉 The EC2 instance now serves my static website from user data!

---
- [x] Confirm the Employee Directory loads (empty state)
---

![Screenshot 2025-07-08 at 16 57 42](https://github.com/user-attachments/assets/d88192c7-8134-4226-bd85-9b557a60d86a)

---

## 🌐 Module 3: VPC Networking + Re-deploy

#### 🛠️ VPC Setup
---
- [x] Created custom VPC: `app-vpc`
  - CIDR block: `10.1.0.0/16`
---

![Screenshot 2025-07-09 at 09 57 07](https://github.com/user-attachments/assets/2cd9fb4e-dd8b-4b77-8bdf-cc376432b054)

#### 🧱 Subnet Configuration
---
- [x] Created four subnets with non-overlapping ranges:
  - `Public Subnet 1` → `10.1.1.0/24` (AZ: `e.g. eu-west-2a`)
  - `Private Subnet 1` → `10.1.2.0/24` (AZ: `e.g. eu-west-2a`)
  - `Public Subnet 2` → `10.1.3.0/24` (AZ: `e.g. eu-west-2b`)
  - `Private Subnet 2` → `10.1.4.0/24` (AZ: `e.g. eu-west-2b`)
---

![Screenshot 2025-07-09 at 10 16 06](https://github.com/user-attachments/assets/00960008-5912-49a1-ad9b-ed2511b534db)

![Screenshot 2025-07-09 at 10 00 05](https://github.com/user-attachments/assets/4a57be65-a6c6-420d-a62a-ee1d96417339)

![Screenshot 2025-07-09 at 10 00 20](https://github.com/user-attachments/assets/db6a464c-d36a-40ea-9bb1-972cd3f7c636)

![Screenshot 2025-07-09 at 10 00 44](https://github.com/user-attachments/assets/df10dc5c-5a59-403b-8934-df47c0c74a23)



#### 🌐 Internet Gateway
---
- [x] Created and attached Internet Gateway: `app-igw`
  - Attached to `app-vpc`
---

![Screenshot 2025-07-09 at 10 05 17](https://github.com/user-attachments/assets/3619ae1e-df25-40e7-97b8-829b9615b918)

![Screenshot 2025-07-09 at 10 06 06](https://github.com/user-attachments/assets/d999f0e2-2ef5-4182-9bfd-312bfea20e38)

#### 🧭 Public Route Table
---
- [x] Created route table: `public-route-table`
  - Destination: `0.0.0.0/0` → Target: Internet Gateway
  - Associated with:
    - `Public Subnet 1`
    - `Public Subnet 2`
---

![Screenshot 2025-07-09 at 10 09 11](https://github.com/user-attachments/assets/c146de50-a7ca-4359-894f-f4fdb0508416)

![Screenshot 2025-07-09 at 10 10 09](https://github.com/user-attachments/assets/169501f5-d760-4028-ae00-ae8991245132)

![Screenshot 2025-07-09 at 10 10 55](https://github.com/user-attachments/assets/291a3310-35f9-435d-9c72-ace37bd87c64)

> ✅ Reminder: Subnets are only considered "public" if they are associated with a route table that connects them to an Internet Gateway.

**🔄 Preparing the Flask App for EC2 Deployment**

Since I didn’t have access to the original employee-app.zip used in the AWS Technical Essentials course, I decided to recreate the Flask application myself using Gemini. My goal was to:

- 🎯 Recreate the employee directory app structure locally
- 📦 Zip it and upload to my own S3 bucket
- 📝 Reference it in EC2 User Data script
- 🚀 Relaunch the app into my custom VPC using Amazon EC2

**📁 Step 1: Build the Flask App Locally** 

I used Gemini to generate a simple Flask app that includes:

```
employee-app/
├── application.py
├── requirements.txt
├── templates/
│   └── index.html
├── static/
    └── style.css
```

**🗜️ Step 2: Zip the Application**

```bash
cd employee-app
zip -r employee-app.zip .
```

This creates a employee-app.zip file with all the necessary code and folders inside.

**☁️ Step 3: Upload to Amazon S3**

---
- [x] Go to the S3 console
---

![Screenshot 2025-07-09 at 12 09 14](https://github.com/user-attachments/assets/a13ea044-d577-44dd-a69c-e894abd878fc)

---
- [x] Click Create bucket
  - Give it a unique name (e.g. employee-flask-app)
  - Choose the same Region as your EC2 instance (e.g. eu-west-2)
  - Leave the default settings (Block public access ON is fine for now)
---

![Screenshot 2025-07-09 at 12 20 31](https://github.com/user-attachments/assets/718d8778-384f-4687-9695-d14437383b58)

**🔐 Making My S3 Zip File Public for EC2 User Data**
When I got to this stage, I asked myself:

> “Do I need to disable Block Public Access in my S3 bucket to let EC2 download my employee-app.zip file using wget?”

After a bit of digging, here’s what I learned 👇

**✅ Yes — if I want EC2 to download the file using a public URL**
By default, S3 buckets block all public access, which is great for security — but that also means my EC2 instance won’t be able to download my file using:

```bash
wget https://my-bucket-name.s3.amazonaws.com/employee-app.zip
```

Unless I explicitly make that file public, the download will silently fail during the launch process.

---
- [x] Open the newly created bucket
---

![Screenshot 2025-07-09 at 12 21 40](https://github.com/user-attachments/assets/0d1fba15-81ec-4b6e-9d78-51632a043f9f)

---
- [x] Click Upload → Add files
  - Upload your employee-app.zip file
  - Opened the Object actions dropdown ❌ (I had to find another solution, which you will see!)
  - Chose **"Make public"** to allow access only to that specific file ❌ (I had to find another solution, which you will see!)

**🛠️ Making employee-app.zip Public (Using a Bucket Policy Instead of ACL)**

After uploading my employee-app.zip file to S3, I needed to make it publicly accessible so my EC2 instance could download it as part of the **User Data script**.

At first, I tried to use the **“Make public using ACL”** option on the file — but it was greyed out.

![Screenshot 2025-07-09 at 12 27 42](https://github.com/user-attachments/assets/f0e4067b-5518-442d-8a0e-e299892cf8e1)

So here’s what I did instead:

**🔐 Adjusting Bucket Permissions (via Policy)**

1. I went to the Permissions tab of the bucket.
2. Clicked Edit under Block Public Access (bucket settings).
3. I unchecked this one setting:

```
Block public and cross-account access to buckets and objects through any public bucket or access point policies
```

> This setting was preventing even valid bucket policies from allowing public access.

4. Then I scrolled to the **Bucket Policy** section and added the following:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadForObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::employee-flask-app/employee-app.zip"
    }
 ]
}
```

5. I saved the changes and copied the **Object URL** for the file (found under the file’s details).
6. Finally, I opened a **private/incognito browser tab**, pasted the URL, and… ✅ it worked! The browser downloaded the .zip file with no errors.

This confirms that the file is now publicly accessible **(only that one file)** — and I’m ready to use this link inside my EC2 User Data script.

---
- [x] After upload completes:
  - Click on the file
  - Under Object URL, copy the link — for example:
---

```bash
https://employee-flask-app.s3.amazonaws.com/employee-app.zip
```
**🎯 Why This Works:**
This lets my EC2 instance pull the zip file with wget during boot, **without making the whole bucket public.**
Just one secure, targeted object permission — clean and minimal.

Now I’m ready to paste that URL into the EC2 **User Data script** for the next step!

**📝 Step 4: Update the EC2 User Data Script**

Update the launch script to pull your real .zip file from S3:

```bash
#!/bin/bash
cd /home/ec2-user
wget https://employee-flask-app.s3.eu-west-2.amazonaws.com/employee-app.zip
unzip employee-app.zip
cd employee-app
yum install python3 -y
pip3 install -r requirements.txt
yum install stress -y
export PHOTOS_BUCKET=employee-photo-bucket-sr963
export AWS_DEFAULT_REGION=us-west-2
export DYNAMO_MODE=on
python3 application.py
```

**🚀 Step 5: Relaunch EC2 with Updated Script**

In the AWS EC2 Console:

1. Go to Instances → click new instance
2. Rename it: employee-directory-app-networking-module
3. Choose:
  - Instance type: `t2.micro`
  - Proceed without key pair
  - VPC: app-vpc
  - Subnet: Public Subnet 1
  - Auto-assign Public IP: ✅ Enabled
4. Paste your updated User Data into the Advanced Details section
- [x] Created new security group for `app-sg`
  - Inbound rules:
    - HTTP (port 80) from anywhere
    - HTTPS (port 443) from anywhere
    - ssh (port 22) from anywhere
  5. Attach IAM role: EmployeeWebAppRole
    - Grants EC2 instance access to S3 and DynamoDB

**😮‍💨 Step 6: When the Flask App Still Didn’t Work…**

After following all the steps — zipping up my Flask app, making the S3 object public, launching the EC2 instance with the correct IAM role and security group — I was so sure it would finally work.

But…

```
❌ This site can’t be reached  
18.133.156.203 refused to connect.  
ERR_CONNECTION_REFUSED
```

At this point, I genuinely wanted to shed a tear.

I had been battling Gemini’s AI-generated Flask code for nearly **2 hours** — tweaking the structure, rewriting the application.py, rebuilding the zip, fixing the User Data script, redeploying, and still... nothing.

**🧠 Lesson: Sometimes Google > AI**

In a last-ditch effort, I Googled:

> “AWS Technical Essentials Flask code”

And boom 💥 — I found a course article that included **the exact User Data script** used in the original training materials.

**✅ The Working User Data Script (Finally!)**

```bash
#!/bin/bash -ex 
wget https://aws-tc-largeobjects.s3-us-west-2.amazonaws.com/DEV-AWS-MO-GCNv2/FlaskApp.zip 
unzip FlaskApp.zip 
cd FlaskApp/ 
yum -y install python3 
yum -y install python3-pip 
pip install -r requirements.txt 
yum -y install stress 
export PHOTOS_BUCKET=employee-flask-app
export AWS_DEFAULT_REGION=eu-west-2
export DYNAMO_MODE=on 
FLASK_APP=application.py /usr/local/bin/flask run --host=0.0.0.0 --port=80
```

**🎉 And It Worked!**

I updated the User Data with this version, launched a new EC2 instance, and visited the public IP:

> ✅ The Flask Employee Directory loaded perfectly in my browser!

![Screenshot 2025-07-09 at 16 22 12](https://github.com/user-attachments/assets/c83440b5-333b-45a6-b471-a18d17ed1fb4)

**📌 Key Takeaway**

Sometimes, instead of debugging generated code for hours, a simple Google search can save the day — just like the good ol’ StackOverflow era.

---

## 💾 Module 4: Storage (S3 Integration)

#### 🪣 S3 Bucket Creation & Object Upload
---
- [x] Created S3 bucket: `employee-photo-bucket-456s`
  - Region: `eu-west-2` (same as rest of app)
  - Default settings retained (no public access)
---

![Screenshot 2025-07-10 at 10 07 44](https://github.com/user-attachments/assets/bdb038f2-0f2b-4397-94e8-bebac8168c44)

---
- [x] Uploaded test image to validate bucket
  - Used GUI Upload → `employee2.jpg`
  - Verified success in S3 console
---

![Screenshot 2025-07-10 at 10 10 27](https://github.com/user-attachments/assets/0807e89e-dd8a-4ce5-ab45-7e5e79c530e0)

![Screenshot 2025-07-10 at 10 10 44](https://github.com/user-attachments/assets/055b577c-bce3-4bbe-9954-dfcf83438493)

#### 🔐 Bucket Policy Configuration
---
- [x] Navigated to **Permissions** tab → Edited **Bucket Policy**
---

![Screenshot 2025-07-10 at 10 11 48](https://github.com/user-attachments/assets/995e0007-1e47-4675-98a0-3932866001e0)

---
- [x] Customized IAM policy:
  - Replaced `INSERT-ACCOUNT-NUMBER` with actual account number
  - Replaced `INSERT-BUCKET-NAME` with actual bucket name
  - Removed `<>` brackets
- [x] Saved policy to allow access from EC2 via IAM Role (`EmployeeWebAppRole`)
---

**To find the account number Using the AWS Management Console:**
1. Sign in: Access the AWS Management Console using your AWS credentials.
2. Navigate to Support Center: Find and click on the "Support" menu, then select "Support Center".
3. Locate Account ID: Your AWS account ID is displayed prominently at the top of the Support Center page.

**To find the buckect number** 
- it should be right above the policy code, under the title **"Bucket ARN"**

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowS3ReadAccess",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::<INSERT-ACCOUNT-NUMBER>:role/EmployeeWebAppRole"
      },
      "Action": "s3:*",
      "Resource": [
        "arn:aws:s3:::<INSERT-BUCKET-NAME>",
        "arn:aws:s3:::<INSERT-BUCKET-NAME>/*"
      ]
    }
  ]
}
```

![Screenshot 2025-07-10 at 11 50 25](https://github.com/user-attachments/assets/30ab0e10-1fa8-4bda-acc9-ae405ea0bffc)

#### 🔁 EC2 Relaunch: App Configured to Use S3
---
- [x] Cloned existing EC2 instance
  - Used **Launch more like this** on stopped instance
  - Renamed to: `employee-directory-app-s3`
---

![Screenshot 2025-07-10 at 11 52 22](https://github.com/user-attachments/assets/68584f44-9946-46f9-ace6-b61772ad40c3)

I then got an error informing me " (Error: The selected EC2 instance must be running.) " **Good to know!**

![Screenshot 2025-07-10 at 11 53 46](https://github.com/user-attachments/assets/bea98e88-3cf7-4b53-9fb6-64e00920fac4)

![Screenshot 2025-07-10 at 11 56 29](https://github.com/user-attachments/assets/c5a5c6b8-6425-4f71-9aa2-52287d4467f3)

---
- [x] Verified:
  - Same AMI and instance type (`t2.micro`)
  - Auto-assign Public IP → **Enabled**
  - IAM Role pre-populated: `EmployeeWebAppRole`
---
---
#### ⚙️ User Data Configuration
- [x] Updated EC2 user data with S3 bucket name
  - Set environment variable: `PHOTOS_BUCKET=employee-photo-bucket-456s`
  - Launch script pulls app files from S3 and installs dependencies
---
```bash
#!/bin/bash -ex 
wget https://aws-tc-largeobjects.s3-us-west-2.amazonaws.com/DEV-AWS-MO-GCNv2/FlaskApp.zip 
unzip FlaskApp.zip 
cd FlaskApp/ 
yum -y install python3 
yum -y install python3-pip 
pip install -r requirements.txt 
yum -y install stress 
export PHOTOS_BUCKET=employee-photo-bucket-456s
export AWS_DEFAULT_REGION=eu-west-2
export DYNAMO_MODE=on 
FLASK_APP=application.py /usr/local/bin/flask run --host=0.0.0.0 --port=80
```

#### ✅ Validation
---
- [x] Waited for EC2 status checks → **2/2 checks passed**
- [x] Opened public IP in browser
  - ✅ Application launched successfully with S3 bucket integration
  - ❗ Note: Database (DynamoDB) not yet configured for interaction
---

![Screenshot 2025-07-10 at 12 01 45](https://github.com/user-attachments/assets/61d80f11-692d-48f4-9ec0-c41cd8ac3031)

![Screenshot 2025-07-10 at 12 03 00](https://github.com/user-attachments/assets/c76645a3-353f-4e90-9d95-65f3730fa018)

#### 🧹 Cleanup
---
- [x] Stopped demo instance (optional for cost saving)
---

---
## 🗄️ Module 5: Database (DynamoDB Integration)

!-- DynamoDB table creation, full CRUD test via app --
🧹 **Optional:** Finish each module with cleanup steps to avoid unexpected AWS charges!

---

## 📈 Module 6: Monitoring & Auto Scaling

!-- Load balancer setup, ASG, launch template, stress test, scale-out --
🧹 **Optional:** Finish each module with cleanup steps to avoid unexpected AWS charges!
