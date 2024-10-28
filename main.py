from src.welcome import welcome
from src.process import encrypt, decrypt
from src.db import dbcon, dbsave, dbget

def main():
    welcome()

    while True:
        dbpass = input("\nEnter the password to connect to MySQL: ")
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
            key, encdata = encrypt(ptext)
            recid = dbsave(encdata, key, dbpass, dbname)
            print(f"\nEncrypted text: {encdata}")
            print(f"\nData saved with record ID {recid}")

        elif choice == '2':
            try:
                inrec = int(input("\nEnter the record ID to decrypt: "))
                rec = dbget(inrec, dbpass, dbname)
                if rec:
                    ctext, key = rec
                    dctext = decrypt(ctext, key)
                    print(f"\nDecrypted text: {dctext}")
                else:
                    print("\nRecord not found!")
            except ValueError:
                print("\nInvalid record ID. Please try again...")

        elif choice == '3':
            print("\nProcess ended!\n")
            break
        
        else:
            print("\nInvalid choice. Please try again...")

if __name__ == "__main__":
    main()