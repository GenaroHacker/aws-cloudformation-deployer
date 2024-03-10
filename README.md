# aws-cloudformation-deployer 

**Create** an **AWS IAM user** with S3 and CloudFormation full access, generate access keys, and set up AWS CLI v2 and boto3 on Ubuntu. **Deploy a CloudFormation stack using a Python script**.

## Table of Contents

1. [**Create an IAM User with Necessary Permissions**](#step-1-create-an-iam-user-with-necessary-permissions)
2. [**Generate Access Keys**](#step-2-generate-access-keys)
3. [**Install AWS CLI v2 and SDK for Python on Ubuntu**](#step-3-install-aws-cli-v2-and-sdk-for-python-on-ubuntu)
4. [**Configure the AWS CLI**](#step-4-configure-the-aws-cli)
5. [**Deploy the CloudFormation Stack**](#step-5-deploy-the-cloudformation-stack)

## Step 1: Create an IAM User with Necessary Permissions

- **Navigate** to the **AWS Management Console**.
- **Type "IAM"** in the search bar and **select it**.
- Go to "Users" and click on **"Create user"**.
- Name the user **"my_new_user"** and continue.
- Select **"Attach policies directly"** and add `AmazonS3FullAccess` and `AWSCloudFormationFullAccess`.
- Click on "Create user".

## Step 2: Generate Access Keys

- Find the newly created user.
- Click on **"Create access key"**.
- **Select the CLI option** and acknowledge the recommendations.
- Click **"Create access key"** again and securely **store the provided keys**.

## Step 3: Install AWS CLI v2 and SDK for Python on Ubuntu

```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

```bash
pip install boto3
```

```bash
pip install -r requirements.txt
```

## Step 4: Configure the AWS CLI

```bash
aws configure
```
- Provide your Access key ID, Secret access key, and default AWS region.

## Step 5: Deploy the CloudFormation Stack

- **Download** and **open** the **`main.py` file** in your code editor.
- **Execute the file** to deploy the CloudFormation stack.


