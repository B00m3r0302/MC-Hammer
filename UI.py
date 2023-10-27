from blessed import Terminal
from scanner import Scanner
from view_tables import DatabaseViewer

class App:
    def __init__(self):
        self.term = Terminal()
        self.alerts = ["Alert 1: Suspicious activity detected", "Alert 2: High CPU usage"]
        self.scanner = Scanner()

    def clear_screen(self):
        print(self.term.clear())

    def start_scan(self):
        try:
            # TODO: Make Sure this is the right function to call
            self.scanner.Baseline_Scan(start_dir="C:\\")
            print("Scan complete!")
        except Exception as e:
            print(f"An error occurred while starting scan: {str(e)}")

    def view_tables(self):
        self.clear_screen()
        db_viewer = DatabaseViewer()
        db_viewer.display_table_contents()
        db_viewer.close_connection()

        input("\n Press Enter to continue...")

    def add_trusted_connection(self):
        self.scanner.add_trusted_connection()

    def remove_trusted_connection(self):
        self.scanner.remove_trusted_connection()

    def alerts_menu(self):
        self.clear_screen()

        print("Alerts")
        print("------")
        for alert in self.alerts:
            input("\n Press Enter to continue...")

    def run(self):
        while True:
            print("MC-Hammer Incident Detection and Response Tool")
            print("<= You Can't Touch This =>")
            print("---------------------------------------------")
            print("1. Start Scan")
            print("2. View Tables")
            print("3. Add Trusted Connections")
            print("4. Remove Trusted Connection")
            print(f"5. View Alerts ({self.alerts})")  # using f-string for variable substitution
            print("6. Exit")
            print("---------------------------------------------")
            
            choice = input("Enter your choice: ")

            if choice == "1":
                self.start_scan()
            elif choice == "2":
                self.view_tables()
            elif choice == "3":
                self.add_trusted_connection()
            elif choice == "4":
                self.remove_trusted_connection()
            elif choice == "6":
                self.clear_screen()
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    app = App()
    app.run()
