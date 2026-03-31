 ---

  Prerequisites
   * A Linux Server with SSH access.
   * Python 3.10 or higher.
   * PostgreSQL installed and running.

  ---

  Step 1: Install System Dependencies
  Update your system and install the necessary libraries for Python and PostgreSQL.

   1 sudo apt update && sudo apt upgrade -y
   2 sudo apt install -y python3-pip python3-venv git libpq-dev postgresql postgresql-contrib

  ---

  Step 2: Database Setup
  Create the database and the user as specified in your secrets.toml.

   1. Log in to PostgreSQL:
   1     sudo -u postgres psql

   2. Run these SQL commands:

   1     CREATE DATABASE tiktok_dashboard_db;
   2     CREATE USER NMKDEV WITH PASSWORD 'NMKDEV@1718';
   3     GRANT ALL PRIVILEGES ON DATABASE tiktok_dashboard_db TO NMKDEV;
   4     \q

   3. Import your schema:
      If you have your .sql or schema files, apply them now:

   1     psql -U NMKDEV -d tiktok_dashboard_db -f orders_schema.txt

  ---

  Step 3: Application Deployment

   1. Clone the Repository:

   1     cd /var/www
   2     sudo git clone https://github.com/your-repo/streamlit_tiktok_dashboard.git
   3     sudo chown -R $USER:$USER /var/www/streamlit_tiktok_dashboard
   4     cd streamlit_tiktok_dashboard

   2. Setup Virtual Environment:

   1     python3 -m venv venv
   2     source venv/bin/activate
   3     pip install --upgrade pip
   4     pip install -r requirements.txt

  ---

  Step 4: Configuration (Secrets)
  Ensure your .streamlit/secrets.toml is correctly configured on the server.

   1 mkdir -p .streamlit
   2 nano .streamlit/secrets.toml

  Paste your configuration:
   1 [postgresql]
   2 username = "NMKDEV"
   3 password = "NMKDEV@1718"
   4 databasename = "tiktok_dashboard_db"
   5 host = "localhost"
   6 port = 5432

  ---

  Step 5: Create a System Service (Systemd)
  To ensure the dashboard runs automatically in the background and restarts if the server reboots.

   1. Create the service file:

   1     sudo nano /etc/systemd/system/streamlit-app.service

   2. Paste the following (Replace your-user with your actual username):

    1     [Unit]
    2     Description=Streamlit TikTok Dashboard
    3     After=network.target
    4
    5     [Service]
    6     User=your-user
    7     Group=your-user
    8     WorkingDirectory=/var/www/streamlit_tiktok_dashboard
    9     Environment="PATH=/var/www/streamlit_tiktok_dashboard/venv/bin"
   10     ExecStart=/var/www/streamlit_tiktok_dashboard/venv/bin/streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0
   11
   12     [Install]
   13     WantedBy=multi-user.target

   3. Start and Enable the service:

   1     sudo systemctl daemon-reload
   2     sudo systemctl start streamlit-app
   3     sudo systemctl enable streamlit-app

  ---

  Step 6: Firewall & Access
  Open the port 8501 to allow traffic to your dashboard.

   1 sudo ufw allow 8501
   2 sudo ufw status

  You can now access your dashboard at http://your-server-ip:8501.

  ---

  Summary of Maintenance Commands
   * Check status: sudo systemctl status streamlit-app
   * Restart app: sudo systemctl restart streamlit-app
   * View Logs: journalctl -u streamlit-app -f
   * Run DB Cleanup: /var/www/streamlit_tiktok_dashboard/venv/bin/python clean_db.py