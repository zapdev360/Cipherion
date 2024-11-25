from src.welcome import welcome, sep
from src.process import encrypt, decrypt
from src.db import dbcon, dbsave, dbget, dbupdate
from src.utils.mask import maskpass
from src.utils.color import color
from src.utils.table import menutab, algotab

def main():
    welcome()
    
    while True:
        prompt = color('[INPUT]', "Enter the password to connect to MySQL: ", newline=True)
        dbpass = maskpass(prompt)
        dbname = input(color('[INPUT]', "Enter the name of the database: "))
        
        if dbcon(dbpass, dbname):
            break
        else:
            print(color('[FAIL]', "Please try again..."))
    
    while True:
        print('\n', sep, '\n')
        menutab()
        choice = input(color('[INPUT]', "Enter choice (1, 2 or 3): ", newline=True))
        
        if choice == '1':
            while True:
                ptext = input(color('[INPUT]', "Enter the text to encrypt: "))
                if ptext.strip():
                    break
                else:
                    print(color('[INFO]', "Text cannot be empty or contain only whitespace(s)!", newline=True))
                    print(color('[FAIL]', "Please try again...\n"))
            
            print()
            algotab()
            print(color('[INFO]', "Encryption via AES or ChaCha20Poly1305 is recommended, unless you have specific objective(s).", newline=True))
            algchoice = input(color('[INPUT]', "Enter choice (1, 2, 3 or 4): ", newline=True))
            
            if algchoice == '1':
                algo = 'AES'
            elif algchoice == '2':
                algo = 'ChaCha20Poly1305'
            elif algchoice == '3':
                algo = 'Blowfish'
            elif algchoice == '4':
                algo = 'TripleDES'
            else:
                print(color('[FAIL]', "Invalid algorithm choice. Please try again...", newline=True))
                continue
            
            try:
                key, encdata = encrypt(ptext, algo)
                recid = dbsave(encdata, key, algo, dbpass, dbname)
                print(color('[SUCCESS]', f"Encrypted text: {encdata}", newline=True))
                print(color('[SUCCESS]', f"Algorithm: {algo}"))
                print(color('[SUCCESS]', f"Record ID: {recid}"))
            except Exception as e:
                print(color('[FAIL]', f"Error during encryption: {e}", newline=True))
        
        elif choice == '2':
            try:
                inrec = int(input(color('[INPUT]', "Enter the record ID to decrypt: ")))
                rec = dbget(inrec, dbpass, dbname)
                if rec:
                    ctext, key, algo = rec
                    dctext, new_key, new_encdata = decrypt(ctext, key, algo, rotate=True)
                    print(color('[SUCCESS]', f"Decrypted text: {dctext}", newline=True))
                    print(color('[SUCCESS]', f"Algorithm: {algo}"))
                    dbupdate(inrec, new_encdata, new_key, dbpass, dbname)
                    print(color('[SUCCESS]', "Key rotation was successful!"))
                else:
                    print(color('[FAIL]', "Record not found!", newline=True))
            except ValueError:
                print(color('[FAIL]', "Invalid record ID. Please try again...", newline=True))
            except Exception as e:
                print(color('[FAIL]', f"Error during decryption: {e}", newline=True))
        
        elif choice == '3':
            print(color('[INFO]', "Process ended!\n", newline=True))
            break
        
        else:
            print(color('[FAIL]', "Invalid choice. Please try again...", newline=True))

if __name__ == "__main__":
    main()