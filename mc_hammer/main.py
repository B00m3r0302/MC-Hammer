## main.py
import time
from scanner import Scanner
from analysis import Analysis
from menu import Menu
from logger import Logger
from actions import Actions
import sqlite3
import concurrent.futures
import sys 
import sched

# sys.path.append("c:\\users\\hudson\\appdata\\local\\packages\\pythonsoftwarefoundation.python.3.11_qbz5n2kfra8p0\\localcache\\local-packages\\python311\\site-packages")

class Main:
    def __init__(self):
        self.scanner = Scanner("GuardianAngel.db")
        self.analysis = Analysis()
        self.menu = Menu()
        self.logger = Logger()
        self.actions = Actions()
        self.database_path = "GuardianAngel.db"
        self.s = sched.scheduler(time.time, time.sleep)

## TODO: Change code to use the UI that mark is going to build 
## TODO: Build the UI
## TODO: Add behavioral analytics from SnapAttack 
## TODO: Add actions to actions.py based on detections from SnapAttack analytics 
## TODO: Find a way to include an AI agent, LLM, or ML into the program with deep learning and a neural network.  If not possible at this time then we should focus on ML and training the model against current detections with the automated responses. 
## TODO: Create an 'Alerts' table that combines all of the information from the other discrepancies tables into a single table for ease of use and viewing.
    def connection_handler(self):
        with sqlite3.connect(self.database_path) as conn:
            cursor = conn.cursor()
        trusted_IP = self.actions.fetch_trusted_IPs(self.database_path)
        current_connections = self.scanner.get_current_connections()
        for ip in current_connections:
            if ip not in trusted_IP:
                self.logger.log(f"Blocking IP {ip}")
                self.actions.block_IP(ip)
     
    def baseline_scan(self):
        start_directory = "C:\\"
        self.scanner.Baseline_Scan(start_directory)
        
    def scheduled_file_scan(self):
        self.baseline_scan()
        self.s.enter(7200, 1, self.scheduled_file_scan, ())
        
    def scheduled_scan(self):
        self.connection_handler()
        self.scanner.Continuous_Scan()
        self.s.enter(900, 1, self.scheduled_scan, ())

    def run(self):
        try:
            # Initial scan
            self.baseline_scan()
            self.connection_handler()
            self.scanner.Continuous_Scan()
            
            # Continuous scans
            self.scheduled_scan()
            self.scheduled_file_scan()
            
            # Scheduling
            self.s.enter(7200, 1, self.scheduled_file_scan, ()) # Schedule the file scan to happen every 2 hours
            self.s.enter(900, 1, self.scheudled_scan, ())
            self.s.run()

        except Exception as e:
            self.logger.log(f"An error occurred during scheduled scan: {str(e)}")

if __name__ == "__main__":
    main = Main()
    main.run()