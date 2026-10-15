#!/bin/bash
set -euo pipefail

APP_DIR="/home/ubuntu/student-result-predictor"
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-venv python3-pip nginx

chown -R ubuntu:ubuntu "$APP_DIR"
sudo -u ubuntu python3 -m venv "$APP_DIR/venv"
sudo -u ubuntu "$APP_DIR/venv/bin/pip" install --upgrade pip
sudo -u ubuntu "$APP_DIR/venv/bin/pip" install -r "$APP_DIR/requirements.txt"

cd "$APP_DIR"
sudo -u ubuntu "$APP_DIR/venv/bin/python" train.py

cat > /etc/systemd/system/student-app.service <<'EOF'
[Unit]
Description=Student Result Predictor Flask App
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/student-result-predictor
ExecStart=/home/ubuntu/student-result-predictor/venv/bin/gunicorn --workers 2 --bind 127.0.0.1:5000 app:app
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

cat > /etc/nginx/sites-available/student-app <<'EOF'
server {
    listen 80 default_server;
    server_name _;
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

ln -sf /etc/nginx/sites-available/student-app /etc/nginx/sites-enabled/student-app
rm -f /etc/nginx/sites-enabled/default
systemctl daemon-reload
nginx -t
systemctl enable nginx
systemctl restart nginx
