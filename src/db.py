import mysql.connector as mycon
from src.utils.color import color

def dbcon(dbpass, dbname):
    try:
        print(color('[INFO]', "Initiating database connection...", newline=True))
        con = mycon.connect(host='localhost', user='root', password=dbpass)
        cursor = con.cursor()
        cursor.execute("SHOW DATABASES LIKE %s", (dbname,))
        if cursor.fetchone():
            print(color('[INFO]', f"Database '{dbname}' already exists."))
            print(color('[SUCCESS]', f"Connected to database '{dbname}'.",newline=True))
        else:
            cursor.execute(f"CREATE DATABASE {dbname}")
            print(color('[SUCCESS]', f"Database '{dbname}' created!", newline=True))
            print(color('[SUCCESS]', f"Connected to database '{dbname}'."))

        con.database = dbname
        cursor.close()
        con.close()
        return True
    
    except mycon.Error as err:
        if err.errno == mycon.errorcode.ER_ACCESS_DENIED_ERROR:
            print(color('[FAIL]', "Incorrect password or access denied!", newline=True))
        else:
            print(color('[FAIL]', f"An unexpected error occurred: {err}", newline=True))
        return False

def dbsave(encdata, key, algo, dbpass, dbname):
    try:
        con = mycon.connect(host='localhost', user='root', password=dbpass, database=dbname)
        cursor = con.cursor()
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
        con.commit()
        recid = cursor.lastrowid
        cursor.execute('''INSERT INTO algo (id, algorithm) VALUES (%s, %s)''', (recid, algo))
        con.commit()
        cursor.close()
        con.close()
        return recid
    
    except mycon.Error as err:
        print(color('[FAIL]', f"An error occurred while saving data: {err}", newline=True))
        return None

def dbget(inrec, dbpass, dbname):
    try:
        con = mycon.connect(host='localhost', user='root', password=dbpass, database=dbname)
        cursor = con.cursor()
        cursor.execute('''SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = %s AND table_name = 'data' ''', (dbname,))
        if cursor.fetchone()[0] == 0:
            print(color('[INFO]', "Make sure to encrypt data before trying to decrypt.", newline=True))
            print(color('[FAIL]', f"No data exists in the database '{dbname}'!"))
            cursor.close()
            con.close()
            return None
        
        cursor.execute('''SELECT data.ctext, data.`key`, algo.algorithm 
                          FROM data
                          JOIN algo ON data.id = algo.id
                          WHERE data.id = %s''', (inrec,))
        res = cursor.fetchone()
        cursor.close()
        con.close()
        return res
    
    except mycon.Error as err:
        print(color('[FAIL]', f"An error occurred while retrieving data: {err}", newline=True))
        return None

def dbupdate(recid, encdata, key, dbpass, dbname):
    try:
        con = mycon.connect(host='localhost', user='root', password=dbpass, database=dbname)
        cursor = con.cursor()
        
        cursor.execute('''UPDATE data SET ctext = %s, `key` = %s WHERE id = %s''', (encdata, key, recid))
        con.commit()
        
        if cursor.rowcount == 0:
            print(color('[FAIL]', "No record found with the provided ID. Update failed.", newline=True))
        else:
            print(color('[INFO]', f"Initiating key rotation with record ID {recid}...", newline=True))
            print(color('[SUCCESS]', f"Record ID {recid} updated successfully!", newline=True))
        
        cursor.close()
        con.close()
    
    except mycon.Error as err:
        print(color('[FAIL]', f"An error occurred while updating data: {err}", newline=True))
        return None