from blessed import Terminal
from scanner import Scanner
from view_tables import DatabaseViewer

def display_menu_options(alert_count=0):
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

def trusted_connection_option():
    print("\n1. Add")
    print("2. Remove")
    choice = input("Do you want to add or remove a trusted connection? (Enter number): ")

    if choice == "1":
        ip_address = input("Enter the IP address to add: ")
        # Logic to add the IP address to your data structure or database goes here
        print(f"{ip_address} has been added!")
    elif choice == "2":
        id_number = input("Enter the ID of the trusted connection to remove: ")
        # Logic to remove the trusted connection using the ID goes here
        print(f"Trusted connection with ID {id_number} has been removed!")
    else:
        print("Invalid choice.")

def view_tables():
    print("\n1. BaselineExecutables")
    print("2. Baseline Accounts")
    print("3. BaselineAutoRuns")
    print("4. Discrepancies")
    print("5. Current Connections")
    print("6. Trusted Accounts")
    choice = input("Which table would you like to see? (Enter number): ")

    if choice == "6":
        # This is a hardcoded example. In a real application, you'd retrieve this data from a database.
        print("\nid     IPAddress\n1      127.0.0.1")
    else:
        # Placeholder for the other table views. Implement as needed.
        print(f"Showing data for table option {choice}...")

def main():
    while True:
        alert_count = 0  # Example alert count. You can replace this with actual count.
        choice = display_menu_options(alert_count)

        if choice == "3":
            view_tables()
        elif choice == "4":
            trusted_connection_option()
        elif choice == "6":
            print("Exiting program...")
            break
        else:
            # Placeholder for other functionalities (e.g., start scan, stop scan, etc.)
            print(f"You chose option {choice}")

        input("\nPress Enter to continue...")  # This is to pause the loop and let user read the output

if __name__ == "__main__":
    main()
