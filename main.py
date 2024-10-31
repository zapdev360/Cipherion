from src.welcome import welcome
from src.process import encrypt, decrypt
from src.db import dbcon, dbsave, dbget
from src.utils.input_utils import get_password
def main():
    welcome()
    
    while True:
        prompt = "\nEnter the password to connect to MySQL: " # password prompt
        dbpass = get_password(prompt)
        dbname = input("Enter the name of the database: ")
        if dbcon(dbpass, dbname):
            break
        else:
            print("Please try again...")
    
    while True:
        print("\nChoices:\n1. Encrypt Data\n2. Decrypt Data\n3. Exit")
        choice = input("\nEnter choice (1, 2 or 3): ")
        
        if choice == '1':
            while True:
                ptext = input("\nEnter the text to encrypt: ")
                if ptext.strip():
                    break
                else:
                    print("\nText cannot be empty or contain only whitespace(s).\nPlease try again...")
            
            print("\nChoose encryption algorithm:")
            print("1. AES\n2. TripleDES\n3. Blowfish")
            alg_choice = input("\nEnter choice (1, 2, or 3): ")
            
            if alg_choice == '1':
                algorithm = 'AES'
            elif alg_choice == '2':
                algorithm = 'TripleDES'
            elif alg_choice == '3':
                algorithm = 'Blowfish'
            else:
                print("\nInvalid algorithm choice. Please try again...")
                continue
            
            # Encrypt the data
            try:
                key, encdata = encrypt(ptext, algorithm)  # Updated to match the new function signature
                recid = dbsave(encdata, key, algorithm, dbpass, dbname)
                print(f"\nEncrypted text: {encdata}")
                print(f"\nData saved with record ID {recid} and algorithm {algorithm}")
            except Exception as e:
                print(f"\nError during encryption: {e}")
        
        elif choice == '2':
            try:
                inrec = int(input("\nEnter the record ID to decrypt: "))
                rec = dbget(inrec, dbpass, dbname)
                if rec:
                    ctext, key, algorithm = rec
                    dctext = decrypt(ctext, key, algorithm)
                    print(f"\nDecrypted text: {dctext}")
                else:
                    print("\nRecord not found!")
            except ValueError:
                print("\nInvalid record ID. Please try again...")
            except Exception as e:
                print(f"\nError during decryption: {e}")
        
        elif choice == '3':
            print("\nProcess ended!\n")
            break
        
        else:
            print("\nInvalid choice. Please try again...")

if __name__ == "__main__":
    main()
