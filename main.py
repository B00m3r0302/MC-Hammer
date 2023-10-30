## main.py
import time
from scanner import Scanner
from analysis import Analysis
from logger import Logger
from actions import Actions
from ui import App
from database import Database
import sqlite3
import concurrent.futures
import sys 
import sched
import threading
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

database = Database()
scanner = Scanner()
db_name = "GuardianAngel.db"
app = App()
exit_flag = threading.Event()

## TODO: Build the UI
## TODO: Add behavioral analytics from SnapAttack 
## TODO: Add actions to actions.py based on detections from SnapAttack analytics 
## TODO: Find a way to include an AI agent, LLM, or ML into the program with deep learning and a neural network.  If not possible at this time then we should focus on ML and training the model against current detections with the automated responses. 
## TODO: Create an 'Alerts' table that combines all of the information from the other discrepancies tables into a single table for ease of use and viewing.

def run_scanner(db_name):
    # Create a SQLAlchemy engine and session
    engine = create_engine(f"sqlite:///{db_name}", poolclass=QueuePool)
    Session = sessionmaker(bind=engine)

    while not exit_flag.is_set():
        # Create a new session for each loop iteration 
        session = Session()
        try:
            scanner.Baseline_Scan("C:\\")
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error in scanner: {e}")
        finally:
            session.close()
        
        time.sleep(600)

# Start the scanner in a separate thread so that it starts and runs at the same time as the UI which is when the script is run
scanner_thread = threading.Thread(target=run_scanner)
scanner_thread.daemon = True
scanner_thread.start()

def connection_handler(self):
    with sqlite3.connect(self.database_path) as conn:
        cursor = conn.cursor()
    trusted_IP = self.actions.fetch_trusted_IPs(self.database_path)
    current_connections = self.scanner.get_current_connections()
    for ip in current_connections:
        if ip not in trusted_IP:
            self.logger.log(f"Blocking IP {ip}")
            self.actions.block_IP(ip)

def run():
    print("Welcome to MC-Hammer")
    # Automatically run the UI
    app.run()

    # Set the exit flag to signal the scanner to exit
    exit_flag.set()


if __name__ == "__main__":
    database.create_tables()
    scanner.add_trusted_connection()
    run()