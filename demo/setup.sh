#!/bin/bash

# Update system packages
sudo apt-get update
sudo apt-get upgrade -y

# Install Python, pip, and venv
sudo apt-get install -y python3-pip python3-dev python3-venv build-essential

# Install Node.js and npm
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install PM2 globally
sudo npm install -g pm2

# Install nginx
sudo apt-get install -y nginx

# Setup Backend with virtual environment
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r ../../requirements.txt
deactivate

# Create backend start script (in demo directory)
cd ..
echo '#!/bin/bash
cd "$(dirname "$0")/backend"
source venv/bin/activate
python3 -m uvicorn bny_capstone_crew:app --host 0.0.0.0 --port 8000
deactivate' > start-backend.sh
chmod +x start-backend.sh

# Setup Frontend
cd frontend
# Install dependencies and build
npm install
NODE_ENV=production npm run build

# Create frontend start script (in demo directory)
cd ..
echo '#!/bin/bash
cd "$(dirname "$0")/frontend"
NODE_ENV=production ./node_modules/.bin/next start -p 3000' > start-frontend.sh
chmod +x start-frontend.sh

# Setup nginx configuration
sudo tee /etc/nginx/sites-available/fomc-simulator << EOF
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
    }
}
EOF

# Enable the nginx site
sudo ln -sf /etc/nginx/sites-available/fomc-simulator /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx

# Setup PM2 to run both services
pm2 start ./start-backend.sh --name fomc-backend
pm2 start ./start-frontend.sh --name fomc-frontend
pm2 startup
pm2 save 