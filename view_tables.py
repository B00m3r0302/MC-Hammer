from prettytable import PrettyTable
import sqlite3

class DatabaseViewer:
    def __init__(self, db_name="GuardianAngel.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
    
    def show_tables(self):
        # Query to retrieve all table names
        self.cursor.execute("SELECT name FROM sqlite_master WHERE TYPE='table';")

        tables = self.cursor.fetchall()
        if tables:
            print("Tables in the database:")
            print("-----------------------")
            for table in tables:
                print(table[0])
            print("-----------------------")
        else:
            print("No tables found in the database.")

    def display_table_contents(self):
        # Fetch data from the database 
        self.show_tables()
        table_name = input("Enter the name of the table to view: ")
        self.cursor.execute(f"SELECT * FROM {table_name};")
        data = self.cursor.fetchall()

        # Get column names 
        column_names = [description[0] for description in self.cursor.description]

        # Create a PrettyTable object
        table = PrettyTable(column_names)
        for row in data:
            table.add_row(row)
        
        print(table)

    def display_trusted_connections(self):
        # Query TrustedConnections and retrieve all records
        self.cursor.execute("SELECT * FROM TrustedConnections;")

        rows = self.cursor.fetchall()

        table = PrettyTable(["ID", "IP Address"])

        for row in rows:
            table.add_row([row[0], row[1]])

        print(table)

    def close_connection(self):
        self.conn.close()
    
if __name__ == "__main__":
    viewer = DatabaseViewer()
    viewer.display_table_contents()
    viewer.close_connection()