from src.db import DBhandler
from src.process import ProcessHandler
from src.welcome import welcome, sep
from src.utils.mask import maskpass
from src.utils.color import color
from src.utils.table import menutab, algotab

def main():
    dbhandler = DBhandler()
    phandler = ProcessHandler()
    welcome()

    while True:
        prompt = color('[INPUT]', "Enter the password for connecting to MySQL: ", newline=True)
        dbpass = maskpass(prompt)
        dbname = input(color('[INPUT]', "Enter the name of the database: "))
        if dbhandler.connect(dbpass, dbname):
            break
        else:
            print(color('[FAIL]', "Please try again..."))
    
    while True:
        print('\n' + sep + '\n')
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
                key, encdata = phandler.encrypt(ptext, algo)
                recid = dbhandler.save(encdata, key, algo)
                rphrase, rhash = phandler.genrphrase()
                
                dbhandler.saverhash(recid, rhash)
                
                print(color('[SUCCESS]', f"Encrypted text: {encdata}", newline=True))
                print(color('[SUCCESS]', f"Algorithm: {algo}"))
                print(color('[SUCCESS]', f"Record ID: {recid}"))
                print(color('[INFO]', f"Recovery phrase: {rphrase}", newline=True))
                print(color('[INFO]', "Please save this recovery phrase securely, as it won't be shown again!", newline=True))
                
            except Exception as e:
                print(color('[FAIL]', f"Error during encryption: {e}", newline=True))
        
        elif choice == '2':
            try:
                rphrase = input(color('[INPUT]', "Enter the recovery phrase: "))
                rhash = phandler.hashrphrase(rphrase)
                recid = dbhandler.getrecid(rhash)
                
                if recid:
                    rec = dbhandler.get(recid)
                    if rec:
                        ctext, key, algo = rec
                        dctext, newkey, newencdata = phandler.decrypt(ctext, key, algo, rotate=True)
                        print(color('[SUCCESS]', f"Decrypted text: {dctext}", newline=True))
                        print(color('[SUCCESS]', f"Algorithm: {algo}"))
                        dbhandler.update(recid, newencdata, newkey)
                        print(color('[SUCCESS]', "Key rotation was successful!"))
                    else:
                        print(color('[FAIL]', "Record not found!", newline=True))
                else:
                    print(color('[FAIL]', "Invalid recovery phrase. Please try again...", newline=True))
            
            except ValueError:
                print(color('[FAIL]', "Invalid record ID. Please try again...", newline=True))
            except Exception as e:
                print(color('[FAIL]', f"Error during decryption: {e}", newline=True))
        
        elif choice == '3':
            dbhandler.close()
            print(color('[INFO]', "Process ended!\n", newline=True))
            break
        
        else:
            print(color('[FAIL]', "Invalid choice. Please try again...", newline=True))


if __name__ == "__main__":
    main()
