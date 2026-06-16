# Simple Python app with GitHub Actions CI/CD to EC2

This repository contains a minimal Flask app, tests, and a GitHub Actions workflow that runs tests with `pytest` and deploys the app to an EC2 host via SSH.

---

## STEP-BY-STEP COMPLETION GUIDE

### **STEP 1: Initialize Git Repository Locally**

```bash
cd /home/satoru/Projects/github-actions
git init
git add .
git commit -m "Initial commit: Flask app with CI/CD workflow"
```

---

### **STEP 2: Create GitHub Repository**

1. Go to [github.com/new](https://github.com/new)
2. Create a new repository named `github-actions` (or your preferred name)
3. **Do NOT initialize with README, .gitignore, or license** (you already have these)
4. Click **Create Repository**

---

### **STEP 3: Push Code to GitHub**

```bash
# Add the remote
git remote add origin https://github.com/YOUR_USERNAME/github-actions.git

# Rename branch to main if needed
git branch -M main

# Push code
git push -u origin main
```

---

### **STEP 4: Set Up EC2 Instance (AWS)**

#### 4a. Launch EC2 Instance

1. Go to [AWS EC2 Console](https://console.aws.amazon.com/ec2/)
2. Click **Launch Instances**
3. Choose **Ubuntu 22.04 LTS** (or Amazon Linux 2)
4. Instance type: **t2.micro** (free tier eligible)
5. Configure security group:
   - Allow **SSH (port 22)** from your IP or anywhere (0.0.0.0/0)
   - Allow **Custom TCP (port 8000)** from anywhere (for app access)
6. Review and **Launch**
7. Create/select a key pair (e.g., `my-ec2-key.pem`) and download it

#### 4b. Set Permissions on Local Machine

```bash
# Secure your EC2 key (on your local machine)
chmod 400 /path/to/my-ec2-key.pem
```

#### 4c. SSH into EC2 and Set Up Python

```bash
# SSH into EC2
ssh -i /path/to/my-ec2-key.pem ubuntu@<EC2_PUBLIC_IP>

# Once inside EC2, run:
sudo apt update
sudo apt install -y python3 python3-pip python3-venv

# Create app directory
mkdir -p ~/app
chmod 755 ~/app

# Create .ssh directory for authorized keys
mkdir -p ~/.ssh
chmod 700 ~/.ssh
```

---

### **STEP 5: Create SSH Key Pair for GitHub Actions**

#### 5a. Generate SSH Key (on your local machine)

```bash
# Generate a new SSH key pair (no passphrase)
ssh-keygen -t ed25519 -f ~/.ssh/github-actions-ec2 -N ""
```

This creates two files:
- `~/.ssh/github-actions-ec2` (private key)
- `~/.ssh/github-actions-ec2.pub` (public key)

#### 5b. Add Public Key to EC2

```bash
# Copy the public key content
cat ~/.ssh/github-actions-ec2.pub

# SSH into EC2 again and add it
ssh -i /path/to/my-ec2-key.pem ubuntu@<EC2_PUBLIC_IP>

# Once inside EC2:
echo "YOUR_PUBLIC_KEY_CONTENT_HERE" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
chmod 700 ~/.ssh

# Verify by exiting and testing new key
exit

# Test the new SSH key from local machine
ssh -i ~/.ssh/github-actions-ec2 ubuntu@<EC2_PUBLIC_IP>
# You should connect without password
exit
```

---

### **STEP 6: Add GitHub Secrets**

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret** and add three secrets:

#### Secret 1: `SSH_PRIVATE_KEY`
- Name: `SSH_PRIVATE_KEY`
- Value: Copy the entire content of `~/.ssh/github-actions-ec2` (the private key file)
  ```bash
  cat ~/.ssh/github-actions-ec2
  ```

#### Secret 2: `EC2_HOST`
- Name: `EC2_HOST`
- Value: Your EC2 instance public IP (e.g., `54.123.45.67`)

#### Secret 3: `EC2_USER`
- Name: `EC2_USER`
- Value: `ubuntu` (or `ec2-user` if using Amazon Linux)

---

### **STEP 7: Test the Workflow**

#### 7a. Make a Small Change and Push

```bash
# On your local machine
cd /home/satoru/Projects/github-actions

# Make a small change (e.g., update README)
echo "# Deployed!" >> README.md

# Commit and push
git add README.md
git commit -m "Test workflow trigger"
git push origin main
```

#### 7b. Monitor the Workflow

1. Go to your GitHub repository
2. Click **Actions** tab
3. You should see your workflow running
4. Watch the progress:
   - **Test job** runs first (pytest)
   - **Deploy job** runs after (if tests pass)

#### 7c. Check Real-Time Logs

- Click the workflow run
- Click **test** or **deploy** to see detailed logs

---

### **STEP 8: Verify Deployment on EC2**

```bash
# SSH into EC2
ssh -i ~/.ssh/github-actions-ec2 ubuntu@<EC2_PUBLIC_IP>

# Check if app is running
ps aux | grep app.py

# Check logs
tail -f ~/app/app.log

# Test the app locally on EC2
curl http://localhost:8000/

# Test from your local machine
curl http://<EC2_PUBLIC_IP>:8000/
```

Expected response:
```json
{"message":"Hello from Flask!"}
```

---

### **STEP 9: Troubleshooting**

#### Workflow fails at "Run tests"
- Check: Are all dependencies in `requirements.txt`?
- Fix: Update requirements.txt and push again

#### Workflow fails at "Sync files to EC2"
- Check: Are the GitHub secrets set correctly?
- Check: Does the EC2 key allow passwordless SSH?
- Fix: Test manually from your machine:
  ```bash
  ssh -i ~/.ssh/github-actions-ec2 ubuntu@<EC2_HOST>
  ```

#### App doesn't start on EC2
- SSH into EC2 and check logs:
  ```bash
  cat ~/app/app.log
  ```
- Ensure port 8000 is not already in use:
  ```bash
  sudo lsof -i :8000
  ```

---

### **STEP 10: Production Improvements (Optional)**

For a real production setup, consider:

1. **Use Systemd Service** instead of `nohup`
2. **Use Gunicorn** for production WSGI server
3. **Add SSL/HTTPS** with nginx reverse proxy
4. **Use Docker** for consistent deployments
5. **Add monitoring** (CloudWatch, uptime checks)

---

## Quick Reference

| Item | Value | Where to Get |
|------|-------|-------------|
| `SSH_PRIVATE_KEY` | Content of `~/.ssh/github-actions-ec2` | Your local machine |
| `EC2_HOST` | EC2 public IP | AWS Console |
| `EC2_USER` | `ubuntu` or `ec2-user` | Depends on AMI |
| App URL | `http://<EC2_HOST>:8000/` | After deployment |
# App Deployed!
