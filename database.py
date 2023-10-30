import sqlite3

class Database:
    def __init__(self, db_name='GuardianAngel.db'):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
    
    def create_tables(self):
        # Create the BaselineExecutables table if it doesn't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS BaselineExecutables (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                path TEXT NOT NULL,
                md5_hash TEXT
            )
        ''')
        self.conn.commit()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS ExecutableDiscrepancies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                path TEXT NOT NULL,
                md5_hash TEXT
            )
        ''')
        self.conn.commit()
        
        # Create the BaselineAccounts table if it doesn't exist 
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS BaselineAccounts(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                AccountCreationDate TEXT NOT NULL
            )
        ''')
        self.conn.commit()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS CurrentAccounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                AccountCreationDate TEXT NOT NULL
            )
        ''')
        self.conn.commit()
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS AccountDiscrepancies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                AccountCreationDate TEXT NOT NULL
            )
        ''')
        self.conn.commit()
        
        # Create the TrustedConnections table if it doesn't exist
        self.cursor.execute(''''
            CREATE TABLE IF NOT EXISTS TrustedConnections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                IPAddress TEXT UNIQUE NOT NULL
            )
        ''')
        self.conn.commit()

        # Create the Connections table if it doesn't exist
        self.cursor.execute('''
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
        self.conn.commit()

        # Create the CurrentConnections table if it doesn't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS CurrentConnections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                local_ip TEXT NOT NULL,
                local_port TEXT NOT NULL,
                remote_ip TEXT NOT NULL,
                remote_port TEXT NOT NULL
            )
        ''')
        self.conn.commit()
        
        # Create the autoruns table if it doesn't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS autoruns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                value TEXT NOT NULL
            )
        ''')
        self.conn.commit()
        if __name__ == "__main__":
            database = Database()
            database.create_tables()