#!/bin/bash

# Update system packages
sudo apt-get update
sudo apt-get upgrade -y

# Install Python and pip
sudo apt-get install -y python3-pip python3-dev build-essential

# Install Node.js and npm
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install PM2 globally
sudo npm install -g pm2

# Install nginx
sudo apt-get install -y nginx

# Setup Backend
cd backend
pip3 install -r ../requirements.txt

# Create backend start script
echo '#!/bin/bash
cd backend
python3 -m uvicorn bny_capstone_crew:app --host 0.0.0.0 --port 8000' > start-backend.sh
chmod +x start-backend.sh

# Setup Frontend
cd ../frontend
npm install
npm run build

# Create frontend start script
echo '#!/bin/bash
cd frontend
npx next start -p 3000' > ../start-frontend.sh
chmod +x ../start-frontend.sh

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
sudo ln -s /etc/nginx/sites-available/fomc-simulator /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx

# Setup PM2 to run both services
pm2 start start-backend.sh --name fomc-backend
pm2 start start-frontend.sh --name fomc-frontend
pm2 startup
pm2 save 