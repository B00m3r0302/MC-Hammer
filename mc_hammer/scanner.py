import os
import difflib
import hashlib
import sqlite3

class Scanner:
    def __init__(self):
        pass

    def scan(self):
        conn = sqlite3.connect('valkrie.db')
        cursor = conn.cursor()
        
        cursor.execute('''
                        CREATE TABLE IF NOT EXISTS BselineExecutables(
                            id INTEGER PRIMARY KEY, 
                            FileName TEXT NOT NULL,
                            FilePath TEXT NOT NULL,
                            MD5Hash TEXT NOT NULL
                            )
                        ''')
        for root, dirs, files in os.walk('/'):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    if is_executable(file_path):
                        md5_hash = get_md5_hash(file_path)
                        print(f"File Name: {file}")
                        print(f"File Path: {file_path}")
                        print(f"MD5 Hash: {md5_hash}")
                        print('-' * 50)
                        
                        cursor.execute('''
                                       INSERT INTO BaselineExecutables (FileName, FilePath, MD5Hash)
                                       VALUES (?, ?, ?)
                                       ''', (file, file_path, md5_hash))
                except PermissionError:
                    continue
        conn.commit()
        conn.close()

    def compare(self, current_scan, base_scan):
        """
        Compare the current scan with the base scan.
        Returns a list of discrepancies.
        """
        diff = difflib.unified_diff(base_scan, current_scan)
        discrepancies = list(diff)
        return discrepancies
    
    def get_md5_hash(file_path):
        hash_md5 = hashlib.md5()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    def is_executable(file_path):
        return os.path.isfile(file_path) and os.access(file_path, os.X_OK)
    
    