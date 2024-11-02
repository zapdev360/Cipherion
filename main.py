from src.welcome import welcome, sep
from src.process import encrypt, decrypt
from src.db import dbcon, dbsave, dbget
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
            print(color('[INFO]', "Encryption via AES is recommended, unless you have specific objective(s).", newline=True))
            algchoice = input(color('[INPUT]', "Enter choice (1, 2 or 3): ", newline=True))
            
            if algchoice == '1':
                algorithm = 'AES'
            elif algchoice == '2':
                algorithm = 'TripleDES'
            elif algchoice == '3':
                algorithm = 'Blowfish'
            else:
                print(color('[FAIL]', "Invalid algorithm choice. Please try again...", newline=True))
                continue
            
            try:
                key, encdata = encrypt(ptext, algorithm)
                recid = dbsave(encdata, key, algorithm, dbpass, dbname)
                print(color('[SUCCESS]', f"Encrypted text: {encdata}", newline=True))
                print(color('[SUCCESS]', f"Algorithm: {algorithm}"))
                print(color('[SUCCESS]', f"Record ID: {recid}"))
            except Exception as e:
                print(color('[FAIL]', f"Error during encryption: {e}", newline=True))
        
        elif choice == '2':
            try:
                inrec = int(input(color('[INPUT]', "Enter the record ID to decrypt: ")))
                rec = dbget(inrec, dbpass, dbname)
                if rec:
                    ctext, key, algorithm = rec
                    dctext = decrypt(ctext, key, algorithm)
                    print(color('[SUCCESS]', f"Decrypted text: {dctext}", newline=True))
                    print(color('[SUCCESS]', f"Algorithm: {algorithm}"))
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
