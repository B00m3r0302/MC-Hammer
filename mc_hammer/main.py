## main.py
import schedule
import time
from scanner import Scanner
from analysis import Analysis
from menu import Menu
from logger import Logger
from actions import Actions
import sqlite3
import concurrent.futures

class Main:
    def __init__(self):
        self.scanner = Scanner("GuardianAngel.db")
        self.analysis = Analysis()
        self.menu = Menu()
        self.logger = Logger()
        self.actions = Actions()
        self.database_path = "GuardianAngel.db"

## TODO: Change code to use the UI that mark is going to build 
## TODO: Change the run and scheduled scans so that they support different timings for the different scans
## TODO: Figure out the timings for the different scans. Thinking a connection scan should happen more frequently than a file scan maybe every 10 minutes or so since this would be one of the easiest ways to identify a breach.  Currently the file scan takes about 2 hours at least on my computer so we should create an interval for that that is not so resource intensive on the system 
## TODO: Build the UI
## TODO: Add behavioral analytics from SnapAttack
## TODO: Add complete the actions functions for automated responses to detections. 
## TODO: Add actions to actions.py based on detections from SnapAttack analytics 
## TODO: Find a way to include an AI agent, LLM, or ML into the program with deep learning and a neural network.  If not possible at this time then we should focus on ML and training the model against current detections with the automated responses. 
## TODO: Create an 'Alerts' table that combines all of the information from the other discrepancies tables into a single table for ease of use and viewing.
## TODO: Build the requirements.txt file for the project
    def run(self):
        try:
            # Initial scan
            start_directory = "C:\\"
            self.scanner.Baseline_Scan(start_directory)

            with concurrent.futures.ThreadPoolExecutor() as executor:
                # Start the connection handler every 10 minutes in the thread pool
                schedule.every(10).minutes.do(lambda: executor.submit(self.connection_handler))
                
                # Start the ExecutablesScan every 2.5 hours in the thread pool
                schedule.every(150).minutes.do(lambda: executor.submit(self.scanner.ExecutablesScan))
                
                # Start the Continuous_Scan every 10 minutes in the thread pool
                schedule.every(10).minutes.do(lambda: executor.submit(self.scanner.Continuous_Scan))
                
                while True:
                    schedule.run_pending()
                    time.sleep(1)
        except Exception as e:
            self.logger.log(f"An error occurred during scheduled scan: {str(e)}")
            
    def connection_handler(self):
        with sqlite3.connect(self.database_path) as conn:
            cursor = conn.cursor()
        trusted_IP = self.actions.fetch_trusted_IPs(self.database_path)
        current_connections = self.scanner.get_current_connections()
        for ip in current_connections:
            if ip not in trusted_IP:
                self.logger.log(f"Blocking IP {ip}")
                self.actions.block_IP(ip)
                self.logger.log(f"IP {ip} blocked successfully")
                cursor.execute('''
                                INSERT INTO Blocked_IPs (IP_Address)
                                VALUES (?)
                ''', (ip,))

    #def scheduled_scan(self):
        #try:
            # Perform scan
            #self.connection_handler()
            #self.scanner.ExecutablesScan()
            #self.scanner.Continuous_Scan()
            
            # Compare scan results with base scan
            #self.analysis.get_discrepancies()

            # Log discrepancies

            # Execute actions based on discrepancies

            # Display scan results and discrepancies
            #self.menu.display(scan_results, discrepancies)
        #except Exception as e:
            #self.logger.log(f"An error occurred during scheduled scan: {str(e)}")

if __name__ == "__main__":
    main = Main()
    main.run()