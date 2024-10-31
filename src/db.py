import mysql.connector as mycon

def dbcon(dbpass, dbname):
    try:
        # Connect to MySQL server
        con = mycon.connect(host='localhost', user='root', password=dbpass)
        cursor = con.cursor()
        
        # Check if the database exists
        cursor.execute("SHOW DATABASES LIKE %s", (dbname,))
        if cursor.fetchone():
            print(f"\nDatabase '{dbname}' already exists!\nConnected to database '{dbname}'")
        else:
            cursor.execute(f"CREATE DATABASE {dbname}")
            print(f"\nDatabase '{dbname}' created!\nConnected to database '{dbname}'")
        
        # Use the newly created or existing database
        con.database = dbname
        cursor.close()
        con.close()
        return True
    
    except mycon.Error as err:
        if err.errno == mycon.errorcode.ER_ACCESS_DENIED_ERROR:
            print("\nIncorrect password or access denied!")
        else:
            print("\nAn unexpected error occurred!", err)
        return False

def dbsave(encdata, key, algorithm, dbpass, dbname):
    try:
        # Connect to the specified database
        con = mycon.connect(host='localhost', user='root', password=dbpass, database=dbname)
        cursor = con.cursor()
        
        # Create table if it doesn't exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            ctext TEXT,
            `key` BLOB,
            algorithm VARCHAR(20)
        )''')
        
        # Insert encrypted data into the database
        cursor.execute('''INSERT INTO data (ctext, `key`, algorithm) VALUES (%s, %s, %s)''', (encdata, key, algorithm))
        con.commit()
        recid = cursor.lastrowid
        
        cursor.close()
        con.close()
        return recid
    
    except mycon.Error as err:
        print("\nAn error occurred while saving data:", err)
        return None

def dbget(inrec, dbpass, dbname):
    try:
        # Connect to the specified database
        con = mycon.connect(host='localhost', user='root', password=dbpass, database=dbname)
        cursor = con.cursor()
        
        # Check if the 'data' table exists
        cursor.execute('''SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = %s AND table_name = 'data' ''', (dbname,))
        if cursor.fetchone()[0] == 0:
            print(f"\nNo data exists in the database '{dbname}'")
            print("Make sure to encrypt data before trying to decrypt!")
            cursor.close()
            con.close()
            return None
        
        # Retrieve the encrypted data by record ID
        cursor.execute('''SELECT ctext, `key`, algorithm FROM data WHERE id = %s''', (inrec,))
        res = cursor.fetchone()
        
        cursor.close()
        con.close()
        return res
    
    except mycon.Error as err:
        print("\nAn error occurred while retrieving data:", err)
        return None
