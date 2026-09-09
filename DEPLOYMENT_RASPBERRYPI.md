# Deploying Moretus to Raspberry Pi

A complete guide to deploy the Streamlit application to a Raspberry Pi webserver.

## Prerequisites

- Raspberry Pi (with Raspbian/Raspberry Pi OS installed)
- SSH access to the Pi
- Python 3.8 or higher installed on the Pi
- Internet connection on the Pi

## Step 1: Transfer Project to Raspberry Pi

### Option A: Using Git (Recommended)

1. **Initialize a Git repository** (on your development machine):
   ```bash
   cd c:\msi_projects\moretus
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. **On the Raspberry Pi**, clone the repository:
   ```bash
   cd ~
   git clone <your-repo-url> moretus
   cd moretus
   ```

### Option B: Using SCP (Direct Copy)

Transfer files directly via SCP:
```bash
scp -r c:\msi_projects\moretus pi@192.168.0.xxx:/home/pi/
```

Replace `192.168.0.xxx` with your Pi's IP address.

### Option C: Using Rsync (Best for Updates)

For syncing your local folder with the Pi:
```bash
rsync -avz --delete c:\msi_projects\moretus\ pi@192.168.0.xxx:/home/pi/moretus/
```

## Step 2: Set Up Python Environment on Raspberry Pi

1. **SSH into your Raspberry Pi**:
   ```bash
   ssh pi@192.168.0.xxx
   ```

2. **Install Python development dependencies** (if needed):
   ```bash
   sudo apt-get update
   sudo apt-get install python3-pip python3-venv
   ```

3. **Navigate to project directory**:
   ```bash
   cd ~/moretus
   ```

4. **Create virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

5. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Step 3: Test Streamlit Locally

1. **Run the app locally on the Pi** (with `--server.address 0.0.0.0` to allow external connections):
   ```bash
   streamlit run app.py --server.address 0.0.0.0 --server.port 8501
   ```

2. **Access from another machine** on the network:
   ```
   http://192.168.0.xxx:8501
   ```

Replace `192.168.0.xxx` with your Pi's IP address.

## Step 4: Run Streamlit as a Systemd Service (Persistent)

To make the app run automatically on startup and stay running:

1. **Create a systemd service file**:
   ```bash
   sudo nano /etc/systemd/system/moretus.service
   ```

2. **Paste the following content**:
   ```ini
   [Unit]
   Description=Moretus Streamlit Application
   After=network.target

   [Service]
   Type=simple
   User=pi
   WorkingDirectory=/home/pi/moretus
   Environment="PATH=/home/pi/moretus/venv/bin"
   ExecStart=/home/pi/moretus/venv/bin/streamlit run app.py \
       --server.address 0.0.0.0 \
       --server.port 8501 \
       --logger.level=info \
       --client.showErrorDetails=true
   Restart=always
   RestartSec=10

   [Install]
   WantedBy=multi-user.target
   ```

3. **Save and exit** (Ctrl+X, then Y, then Enter in nano)

4. **Enable and start the service**:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable moretus
   sudo systemctl start moretus
   ```

5. **Check service status**:
   ```bash
   sudo systemctl status moretus
   ```

6. **View logs**:
   ```bash
   sudo journalctl -u moretus -f
   ```

## Step 5: Optional - Set Up Nginx Reverse Proxy

For better stability and to run on port 80:

1. **Install Nginx**:
   ```bash
   sudo apt-get install nginx
   ```

2. **Create Nginx config**:
   ```bash
   sudo nano /etc/nginx/sites-available/moretus
   ```

3. **Paste configuration**:
   ```nginx
   upstream streamlit {
       server 127.0.0.1:8501;
   }

   server {
       listen 80 default_server;
       listen [::]:80 default_server;
       
       server_name _;
       
       location / {
           proxy_pass http://streamlit;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

4. **Enable the site**:
   ```bash
   sudo ln -s /etc/nginx/sites-available/moretus /etc/nginx/sites-enabled/
   sudo rm /etc/nginx/sites-enabled/default
   ```

5. **Test and restart Nginx**:
   ```bash
   sudo nginx -t
   sudo systemctl restart nginx
   ```

Now access your app at `http://192.168.0.xxx` (port 80)

## Step 6: Database and File Persistence

1. **SQLite database location**: The database file (`moretus.db`) will be created in the working directory.

2. **Persistent storage**: Data is stored locally on the Raspberry Pi.

3. **Backup the database regularly**:
   ```bash
   cp ~/moretus/moretus.db ~/moretus/backup_$(date +%Y%m%d).db
   ```

## Troubleshooting

### App won't start
Check logs:
```bash
sudo journalctl -u moretus -n 50
```

### Port 8501 already in use
Change the port in the systemd service file or:
```bash
sudo lsof -i :8501  # Find what's using it
```

### Database locked errors
Ensure only one instance is running:
```bash
ps aux | grep streamlit
```

### Out of memory
Raspberry Pi 4 (2GB) should be sufficient. If needed, increase swap:
```bash
sudo dphys-swapfile swapoff
sudo nano /etc/dphys-swapfile  # Change CONF_SWAPSIZE=2048
sudo dphys-swapfile swapon
```

## Monitoring

### Check if service is running:
```bash
sudo systemctl status moretus
```

### Restart the service:
```bash
sudo systemctl restart moretus
```

### Stop the service:
```bash
sudo systemctl stop moretus
```

## Access Your Application

- **Local Pi**: `http://localhost:8501` or `http://127.0.0.1:8501`
- **From network**: `http://192.168.0.xxx:8501`
- **With Nginx**: `http://192.168.0.xxx` (port 80)
- **With domain**: Configure DNS to point to Pi's IP

## Performance Optimization for Raspberry Pi

1. **Disable CORS warnings** (already done in config.toml)
2. **Enable caching** in Streamlit
3. **Limit concurrent users** with Nginx upstream settings
4. **Monitor resources**:
   ```bash
   htop  # CPU and memory usage
   df -h  # Disk usage
   ```

## Updates & Maintenance

To pull latest changes from Git:
```bash
cd ~/moretus
git pull
# If requirements.txt changed:
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart moretus
```

## Next Steps

- Set up SSL/TLS certificate with Let's Encrypt (if using domain)
- Configure firewall rules (ufw)
- Set up automatic backups of the database
- Monitor uptime with services like Healthchecks.io

## Reference Links

- [Streamlit Deployment Docs](https://docs.streamlit.io/deploy)
- [Raspberry Pi OS Documentation](https://www.raspberrypi.com/documentation/)
- [Systemd Service Management](https://wiki.debian.org/systemd)
- [Nginx Documentation](https://nginx.org/en/docs/)
