import sqlite3

class Database:
    def __init__(self, db_name='mc_hammer.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Scans (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE,
                data TEXT
            )
        """)
        self.conn.commit()

    def store(self, name: str, data: str):
        try:
            self.cursor.execute("""
                INSERT OR REPLACE INTO Scans (name, data) VALUES (?, ?)
            """, (name, data))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {str(e)}")

    def retrieve(self, name: str):
        self.cursor.execute("""
            SELECT data FROM Scans WHERE name = ?
        """, (name,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return None
