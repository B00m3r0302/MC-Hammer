import os
import difflib
import psutil
import hashlib
import sqlite3
import win32net
class Scanner:
    def __init__(self):
        pass

    def get_md5_hash(self, file_path):
        hash_md5 = hashlib.md5()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def is_executable(self, file_path):
        _, ext = os.path.splitext(file_path)
        return os.path.isfile(file_path) and ext.lower() in ['.exe', '.bat', '.cmd', '.msi']

    def BaselineExecutableScan(self):
        conn = sqlite3.connect('Valkrie.db')
        cursor = conn.cursor()
        
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS BaselineExecutables (
                           id INTEGER PRIMARY KEY,
                           FileName TEXT NOT NULL,
                           FilePath TEXT NOT NULL,
                           md5Hash TEXT NOT NULL
                        )
                    ''')
        
        for root, dirs, files in os.walk('C:\\'):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    if self.is_executable(file_path):
                        md5_hash = self.get_md5_hash(file_path)
                        print(f"File Name: {file}")
                        print(f"File Path: {file_path}")
                        print(f"MD5 Hash: {md5_hash}")
                        print('-' * 50)
                        
                        cursor.execute('''
                                       INSERT INTO BaselineExecutables (FileName, FilePath, md5Hash)
                                       VALUES (?, ?, ?)
                        ''', (file, file_path, md5_hash))
                except PermissionError:
                    continue
        
        conn.commit()
        conn.close()

    def CurrentExecutableScan(self):
        conn = sqlite3.connect('Valkrie.db')
        cursor = conn.cursor()
        
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS CurrentExecutables (
                           id INTEGER PRIMARY KEY,
                           FileName TEXT NOT NULL,
                           FilePath TEXT NOT NULL,
                           md5Hash TEXT NOT NULL
                        )
                    ''')
        
        for root, dirs, files in os.walk('C:\\'):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    if self.is_executable(file_path):
                        md5_hash = self.get_md5_hash(file_path)
                        print(f"File Name: {file}")
                        print(f"File Path: {file_path}")
                        print(f"MD5 Hash: {md5_hash}")
                        print('-' * 50)
                        
                        cursor.execute('''
                                       INSERT INTO CurrentExecutables (FileName, FilePath, md5Hash)
                                       VALUES (?, ?, ?)
                        ''', (file, file_path, md5_hash))
                except PermissionError:
                    continue
        
        conn.commit()
        conn.close()

    def get_users():
        users = []
        level = 1
        resume = 0
        while True:
            (user_list, total, resume) = win32net.NetUserEnum(None, level, win32netcon.FILTER_NORMAL_ACCOUNT, resume, win32netcon.MAX_PREFERRED_LENGTH)
            users.extend(user_list)
            if not resume:
                break
        return users
    
    def BaselineUserScan(self):
        users = get_users()
        conn = sqlite3.connect('Valkrie.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS BaselineAccounts (
                id INTEGER PRIMARY KEY,
                UserName TEXT NOT NULL,
                LastLogon TEXT
            )
        ''')
        
        for user in users:
            username = user['name']
            last_logon = user.get('last_logon', None)
            print(f"Username: {username}")
            print(f"Last Logon: {last_logon}")
            print('-' * 50)
            
            cursor.execute('''
                INSERT INTO BaselineAccounts (UserName, LastLogon)
                VALUES (?, ?)
            ''', (username, str(last_logon)))
        
        conn.commit()
        conn.close()
        
    def CurrentUserScan(self):
        users = get_users()
        conn = sqlite3.connect('Valkrie.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS CurrentAccounts (
                id INTEGER PRIMARY KEY,
                UserName TEXT NOT NULL,
                LastLogon TEXT
            )
        ''')
        
        for user in users:
            username = user['name']
            last_logon = user.get('last_logon', None)
            print(f"Username: {username}")
            print(f"Last Logon: {last_logon}")
            print('-' * 50)
            
            cursor.execute('''
                INSERT INTO CurrentAccounts (UserName, LastLogon)
                VALUES (?, ?)
            ''', (username, str(last_logon)))
        
        conn.commit()
        conn.close()
        
    def Baseline_Scan(self):
        self.BaselineExecutableScan()
        self.BaselineUserScan()
    





