# EC2 Deployment Guide for FOMC Simulator

## Prerequisites

1. AWS Account with EC2 access
2. SSH key pair for EC2 instance
3. Your repository credentials (if private)

## EC2 Instance Setup

1. Launch a new EC2 instance with these specifications:
   - Ubuntu Server 22.04 LTS
   - t2.medium or larger (recommended due to model requirements)
   - At least 30GB EBS storage

2. Configure Security Group:
   - Allow SSH (Port 22) from your IP
   - Allow HTTP (Port 80) from anywhere
   - Allow HTTPS (Port 443) from anywhere

## Deployment Steps

1. SSH into your EC2 instance:
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-ip
   ```

2. Copy the deployment files to the instance:
   ```bash
   scp -i your-key.pem -r deploy/* ubuntu@your-ec2-ip:~/
   ```

3. Make the setup script executable and run it:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

4. Set up your environment variables:
   ```bash
   nano ~/.env
   ```
   Add your API keys:
   ```
   OPENAI_API_KEY=your_key_here
   DEEPSEEK_API_KEY=your_key_here
   ```

5. Clone your repository:
   ```bash
   git clone your-repo-url ~/app
   ```

6. The application should now be running and accessible at:
   ```
   http://your-ec2-ip
   ```

## Architecture

The deployment consists of:
- Next.js frontend running on port 3000
- Python backend running on port 8000
- Nginx reverse proxy serving both on port 80

## Maintenance

- Monitor the applications:
  ```bash
  pm2 status
  pm2 logs fomc-frontend
  pm2 logs fomc-backend
  ```

- Restart services:
  ```bash
  pm2 restart fomc-frontend
  pm2 restart fomc-backend
  ```

- Update the application:
  ```bash
  cd ~/app
  git pull
  
  # Update backend
  pip3 install -r requirements.txt
  pm2 restart fomc-backend
  
  # Update frontend
  cd demo/frontend
  npm install
  npm run build
  pm2 restart fomc-frontend
  ```

## Troubleshooting

1. If the application fails to start:
   - Check frontend logs: `pm2 logs fomc-frontend`
   - Check backend logs: `pm2 logs fomc-backend`
   - Verify environment variables: `cat ~/.env`
   - Check nginx logs: `sudo tail -f /var/log/nginx/error.log`

2. If you can't access the application:
   - Verify nginx status: `sudo systemctl status nginx`
   - Check if both services are running: `pm2 status`
   - Verify security group settings
   - Check if the instance's public IP hasn't changed

3. Memory issues:
   - Monitor memory usage: `free -h`
   - Check PM2 memory usage: `pm2 monit`
   - Consider upgrading instance type if needed

4. Common fixes:
   - Nginx issues: `sudo nginx -t && sudo systemctl restart nginx`
   - Frontend build issues: `cd ~/app/demo/frontend && npm run build`
   - Backend dependency issues: `cd ~/app && pip3 install -r requirements.txt` 