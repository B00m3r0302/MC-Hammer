## main.py
import schedule
import time
from scanner import Scanner
from database import Database
from menu import Menu
from logger import Logger
from actions import Actions

class Main:
    def __init__(self):
        self.scanner = Scanner()
        self.database = Database()
        self.menu = Menu()
        self.logger = Logger()
        self.actions = Actions()

    def run(self):
        try:
            # Initial scan
            scan_results = self.scanner.scan()
            self.database.store('base_scan', scan_results)

            # Schedule the scan every 15 minutes
            schedule.every(15).minutes.do(self.scheduled_scan)

            while True:
                schedule.run_pending()
                time.sleep(1)
        except Exception as e:
            self.logger.log(f"An error occurred: {str(e)}")

    def scheduled_scan(self):
        try:
            # Perform scan
            scan_results = self.scanner.scan()

            # Store scan results
            self.database.store('scan_results', scan_results)

            # Compare scan results with base scan
            base_scan = self.database.retrieve('base_scan')
            discrepancies = self.scanner.compare(scan_results, base_scan)

            # Store discrepancies
            self.database.store('discrepancies', discrepancies)

            # Log discrepancies
            self.logger.log(discrepancies)

            # Execute actions based on discrepancies
            self.actions.execute(discrepancies)

            # Display scan results and discrepancies
            self.menu.display(scan_results, discrepancies)
        except Exception as e:
            self.logger.log(f"An error occurred during scheduled scan: {str(e)}")

if __name__ == "__main__":
    main = Main()
    main.run()
