import mysql.connector as mycon
from src.utils.color import color
from mysql.connector.types import RowType
from typing import Optional

class DBhandler:
    dbname: str = None
    con: mycon.MySQLConnection = None
    
    
    def connect(self, dbpass: str, dbname: str) -> bool:
        self.dbname = dbname

        try:
            print(color('[INFO]', "Initiating database connection...", newline=True))
            con = mycon.connect(host='localhost', user='root', password=dbpass)
            cursor = con.cursor()
            cursor.execute("SHOW DATABASES LIKE %s", (dbname,))
            if cursor.fetchone():
                print(color('[INFO]', f"Database '{dbname}' already exists."))
                print(color('[SUCCESS]', f"Connected to database '{dbname}'.", newline=True))
            else:
                cursor.execute(f"CREATE DATABASE {dbname}")
                print(color('[SUCCESS]', f"Database '{dbname}' created!", newline=True))
                print(color('[SUCCESS]', f"Connected to database '{dbname}'."))

            cursor.close()
            con.database = dbname
            self.con = con
            return True

        except mycon.Error as err:
            if err.errno == mycon.errorcode.ER_ACCESS_DENIED_ERROR:
                print(color('[FAIL]', "Incorrect password or access denied!", newline=True))
            else:
                print(color('[FAIL]', f"An unexpected error occurred: {err}", newline=True))
            return False


    def save(self, encdata: str, key: str, algo: str) -> Optional[int]:
        try:
            self.testcon()
            cursor = self.con.cursor()

            cursor.execute('''CREATE TABLE IF NOT EXISTS data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                ctext TEXT,
                `key` BLOB
            )''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS algo (
                id INT PRIMARY KEY,
                algorithm VARCHAR(20),
                FOREIGN KEY (id) REFERENCES data(id)
            )''')
            cursor.execute('''INSERT INTO data (ctext, `key`) VALUES (%s, %s)''', (encdata, key))
            self.con.commit()
            recid = cursor.lastrowid
            cursor.execute('''INSERT INTO algo (id, algorithm) VALUES (%s, %s)''', (recid, algo))
            self.con.commit()
            cursor.close()
            return recid
        
        except mycon.Error as err:
            print(color('[FAIL]', f"An error occurred while saving data: {err}", newline=True))
            return None


    def saverhash(self, recid: int, rhash: bytes) -> Optional[int]:
        try:
            self.testcon()
            cursor = self.con.cursor()

            cursor.execute('''CREATE TABLE IF NOT EXISTS validate (
                id INT PRIMARY KEY,
                hash BLOB,
                FOREIGN KEY (id) REFERENCES data(id)
            )''')
            cursor.execute('''INSERT INTO validate (id, hash) VALUES (%s, %s)''', (recid, rhash))
            self.con.commit()
            cursor.close()
            return recid
        
        except mycon.Error as err:
            print(color('[FAIL]', f"An error occurred while saving recovery hash: {err}", newline=True))
            return None


    def getrecid(self, rhash: bytes) -> Optional[int]:
        try:
            self.testcon()
            cursor = self.con.cursor()

            cursor.execute('''SELECT id FROM validate WHERE hash = %s''', (rhash,))
            res = cursor.fetchone()
            cursor.close()
            return res[0] if res else None
        
        except mycon.Error as err:
            print(color('[INFO]', f"Make sure to encrypt data before trying to decrypt.", newline=True))
            return None


    def get(self, inrec: int) -> Optional[RowType]:
        try:
            self.testcon()
            cursor = self.con.cursor()
            cursor.execute('''SELECT data.ctext, data.`key`, algo.algorithm 
                            FROM data
                            JOIN algo ON data.id = algo.id
                            WHERE data.id = %s''', (inrec,))
            res = cursor.fetchone()
            cursor.close()
            return res
        
        except mycon.Error as err:
            print(color('[FAIL]', f"An error occurred while retrieving data: {err}", newline=True))
            return None


    def update(self, recid, encdata, key) -> None:
        try:
            self.testcon()
            cursor = self.con.cursor()
            cursor.execute('''UPDATE data SET ctext = %s, `key` = %s WHERE id = %s''', (encdata, key, recid))
            self.con.commit()
            if cursor.rowcount == 0:
                print(color('[FAIL]', "No record found with the provided ID. Update failed.", newline=True))
            else:
                print(color('[INFO]', f"Initiating key rotation with record ID {recid}...", newline=True))
                print(color('[SUCCESS]', f"Record ID {recid} updated successfully!", newline=True))
            cursor.close()

        except mycon.Error as err:
            print(color('[FAIL]', f"An error occurred while updating data: {err}", newline=True))


    def testcon(self) -> None:
        if not self.con:
            raise Exception(color('[FAIL]', "Database is not connected!", newline=True))


    def close(self) -> None:
        if self.con:
            self.con.close()
