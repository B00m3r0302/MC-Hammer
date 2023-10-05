import cmd
import sqlite3
import sys
from main import Main

class Menu(cmd.Cmd):
    def __init__(self):
        super().__init__()
        self.prompt = '> '
        self.intro = 'Welcome to the MC Hammer system. Type help or ? to list commands.\n'
        self.scan_results = []
        self.discrepancies = []
        
    def display_menu_options(self, alert_count=0):
        print("MC-Hammer Incident Detection and Response Tool")
        print("---------------------------------------------")
        print("1. Start Scan")
        print("2. Stop Scan")
        print("3. View Tables")
        print("4. Add/Remove Trusted Connections")
        print(f"5. View Alerts ({alert_count})")  # using f-string for variable substitution
        print("6. Exit")
        print("---------------------------------------------")
        choice = input("Enter your choice: ")
        return choice

    def input_check(self, choice):
        choice = choice
        if choice == 1:
            print("Starting scan...")
            main = Main()
            main.run()
        if choice == 2:
            self.stop_scan()
        if choice == "4":
            self.trusted_connection_option()
        if choice == "6":
            print("Exiting program...")
            sys.exit()
            

    def add_trusted_connection(self, ip_address):
        conn = sqlite3.connect('GuardianAngel.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO TrustedConnections (IP_Address) VALUES (?)", (ip_address))
        conn.commit()
        conn.close()

    def remove_trusted_connection(self, id):
        conn = sqlite3.connect('GuardianAngel.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM TrustedConnections WHERE id=?", (id,))
        conn.commit()
        conn.close()

    def trusted_connection_option(self):
        print("\n1. Add")
        print("2. Remove")
    
        choice = input("Do you want to add or remove a trusted connection? (Enter number): ")

        if choice == '1':
            ip_address = input("Enter the IP address to add: ")
            self.add_trusted_connection(ip_address)
            print("IP address added successfully.")
        elif choice == '2':
            id = input("Enter the ID of the row to remove: ")
            self.remove_trusted_connection(id)
            print("Row removed successfully.")
        else:
            print("Invalid choice!")

    def stop_scan(self):
        print("Stopping scan...")
        return

    def help_exit(self):
        print('Exit the application. Shorthand: x q Ctrl-D.')

    def do_show_scan_results(self, inp):
        '''Show the scan results.'''
        for result in self.scan_results:
            print(result)

    def help_show_scan_results(self):
        print('Show the scan results.')

    def do_show_discrepancies(self, inp):
        '''Show the discrepancies.'''
        for discrepancy in self.discrepancies:
            print(discrepancy)

    def help_show_discrepancies(self):
        print('Show the discrepancies.')

    def display(self, scan_results, discrepancies):
        '''Display the scan results and discrepancies.'''
        self.update(scan_results, discrepancies)
        self.cmdloop()

    def update(self, scan_results, discrepancies):
        '''Update the scan results and discrepancies.'''
        self.scan_results = scan_results
        self.discrepancies = discrepancies
