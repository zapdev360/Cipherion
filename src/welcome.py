import pyfiglet

def welcome():
    sep = "-" * 75
    welcmsg = pyfiglet.figlet_format("Cipherion")
    
    print(sep)
    print(welcmsg)
    print(sep)
    print("Welcome to Cipherion!")
    print("A robust tool for encrypting and securely storing sensitive information.")
    print(sep)
