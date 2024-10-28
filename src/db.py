import mysql.connector as mycon

def dbcon(dbpass, dbname):
    try:
        con = mycon.connect(host='localhost', user='root', password=dbpass)
        cursor = con.cursor()
        cursor.execute("SHOW DATABASES LIKE %s", (dbname,))
        
        if cursor.fetchone():
            print(f"\nDatabase '{dbname}' already exists!\nConnected to database '{dbname}'")
        else:
            cursor.execute(f"CREATE DATABASE {dbname}")
            print(f"\nDatabase '{dbname}' created!\nConnected to database '{dbname}'")
        con.close()

        return True
    
    except mycon.Error as err:
        if err.errno == mycon.errorcode.ER_ACCESS_DENIED_ERROR:
            print("\nIncorrect password or access denied!")
        else:
            print("\nAn unexpected error occurred!", err)

        return False

def dbsave(encdata, key, dbpass, dbname):
    con = mycon.connect(host='localhost', user='root', password=dbpass, database=dbname)
    cursor = con.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS data (
        id INT AUTO_INCREMENT PRIMARY KEY,
        ctext TEXT,
        `key` BLOB
    )''')
    cursor.execute('''INSERT INTO data (ctext, `key`) VALUES (%s, %s)''', (encdata, key))
    con.commit()
    recid = cursor.lastrowid
    cursor.close()
    con.close()

    return recid

def dbget(inrec, dbpass, dbname):
    con = mycon.connect(host='localhost', user='root', password=dbpass, database=dbname)
    cursor = con.cursor()
    cursor.execute('''SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = %s AND table_name = 'data' ''', (dbname,))
    if cursor.fetchone()[0] == 0:
        print(f"\nNo data exists in the database '{dbname}'")
        print("Make sure to encrypt data before trying to decrypt!")
        cursor.close()
        con.close()
        
        return None
    
    cursor.execute('''SELECT ctext, `key` FROM data WHERE id = %s''', (inrec,))
    res = cursor.fetchone()
    cursor.close()
    con.close()
    
    return res