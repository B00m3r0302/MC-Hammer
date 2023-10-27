import sqlite3
import psutil
import winreg
import socket
from prettytable import PrettyTable

db_name = "test.db"
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

def create_tables():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Connections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Protocol TEXT NOT NULL,
            Local_Address TEXT NOT NULL,
            Local_Port INTEGER NOT NULL,
            Foreign_Address TEXT,
            Foreign_Port INTEGER,
            State TEXT NOT NULL
        )
    ''')
    conn.commit()
    
def capture_and_store_connection_data():
    local_conn = sqlite3.connect(db_name)
    local_cursor = local_conn.cursor()
    connections = psutil.net_connections(kind='inet')

    conn_data =[]
    seen = set()
    for conn in connections:
        if conn.family == socket.AF_INET:
            if conn.type == socket.SOCK_STREAM:
                protocol = 'TCP'
            elif conn.type == socket.SOCK_DGRAM:
                protocol = 'UDP'
            else:
                protocol = 'UNKNOWN'
        else:
            protocol = 'UNKNOWN'
        local_address, local_port = conn.laddr
        if conn.raddr:
            foreign_address, foreign_port = conn.raddr
        else:
            foreign_address, foreign_port = None, None
        state = conn.status

        data_tuple = (protocol, local_address, local_port, foreign_address, foreign_port, state)

        unwanted_tuple = ('UDP', '0.0.0.0', 0, None, None, 'NONE')
        if data_tuple != unwanted_tuple and data_tuple not in seen:
            conn_data.append(data_tuple)
            seen.add(data_tuple)

    cursor.executemany('''
        INSERT INTO Connections (Protocol, Local_Address, Local_Port, Foreign_Address, Foreign_Port, State)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', conn_data)
    local_conn.commit()

def display_table_contents():
    # Fetch data from the datagbase
    table_name = input("Enter the name of the table to display: ")
    cursor.execute(f"SELECT * FROM {table_name}")
    data = cursor.fetchall()
    
    # Get the column names
    column_names = [description[0] for description in cursor.description]
    
    # Create a PrettyTable object
    table = PrettyTable(column_names)
    for row in data:
        table.add_row(row)
    print(table)
    
create_tables()
capture_and_store_connection_data()
display_table_contents()