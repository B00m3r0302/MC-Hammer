## main.py
import schedule
import time
from scanner import Scanner
from analysis import Analysis
from menu import Menu
from logger import Logger
from actions import Actions

class Main:
    def __init__(self):
        self.scanner = Scanner("GuardianAngel.db")
        self.analysis = Analysis()
        self.menu = Menu()
        self.logger = Logger()
        self.actions = Actions()

    def run(self):
        try:
            # Initial scan
            start_directory = "C:\\"
            self.scanner.Baseline_Scan(start_directory)

            # Schedule the scan every 15 minutes
            schedule.every(15).minutes.do(self.scheduled_scan)

            while True:
                schedule.run_pending()
                time.sleep(1)
        except Exception as e:
            self.logger.log(f"An error occurred: {str(e)}")
            
    def connection_handler(self):
        trusted_IP = self.actions.fetch_trusted_IPs(self.database_path)
        current_connections = self.scanner.get_current_connections()
        for ip in current_connections:
            if ip not in trusted_IP:
                self.logger.log(f"Blocking IP {ip}")
                self.actions.block_IP(ip)

    def scheduled_scan(self):
        try:
            # Perform scan
            self.connection_handler()
            self.scanner.Scan()
            
            # Compare scan results with base scan
            self.analysis.get_discrepancies()

            # Log discrepancies

            # Execute actions based on discrepancies

            # Display scan results and discrepancies
            #self.menu.display(scan_results, discrepancies)
        except Exception as e:
            self.logger.log(f"An error occurred during scheduled scan: {str(e)}")

if __name__ == "__main__":
    main = Main()
    main.run()
