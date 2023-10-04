import subprocess
from logger import logger
import sqlite3

class Actions:
    def __init__(self, database_path):
        self.database_path = database_path
        self.logger = Logger()

    connection = sqlite3.connect(database_path)
    cursor =- connection.cursor()

    def fetch_trusted_IPs(database_path):
        cursor.execute("SELECT IP_Address FROM TrustedConnections")
        trusted_ips = [row[0] for row in cursor.fetchall()]
        connection.close()
        return trusted_ips

    def block_IP(ip):
        try:
            subprocess.check_call(f"netsh advfirewall firewall add rule name=\"Block {ip}\" dir=in interface=any action=block remoteip={ip}", shell=True)
        except subprocess.CalledProcessError as e:
            self.logger.log(f"Error blocking IP {ip}: {e}")
