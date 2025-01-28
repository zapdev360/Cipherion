import pyfiglet

sep = "-" * 80

def welcome():
    welcmsg = pyfiglet.figlet_format("Cipherion")
    
    print(sep)
    print(welcmsg)
    print(sep)
    print("Welcome to Cipherion!")
    print("A robust tool for encrypting and securely storing sensitive information.")
    print(sep)
    print("Made with ❤️  by @zapdev360")
