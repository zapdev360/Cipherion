import pyfiglet
import shutil
from colorama import init, Fore

init(autoreset=True)

width = shutil.get_terminal_size().columns
sep = "-" * width

def welcome():
    welcmsg = pyfiglet.figlet_format(" ".join("CIPHERION"))
    lines = welcmsg.splitlines()
    maxlen = max(len(line) for line in lines)
    pd = (width - maxlen) // 2
    art = "\n".join([line.rjust(len(line) + pd) for line in lines])
    
    text = "Welcome to Cipherion!".center(width)
    desc = "A robust tool for encrypting and securely storing sensitive information.".center(width)
    cred = "Developed by @zapdev360\n".center(width)
    
    print("\n" + Fore.LIGHTBLUE_EX + art)
    print(sep)
    print(text)
    print(desc)
    print(sep)
    print(cred)
