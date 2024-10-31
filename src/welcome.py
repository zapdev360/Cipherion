import pyfiglet
import shutil

def welcome():
    # Get the terminal width to make the separator dynamic
    terminal_width = shutil.get_terminal_size().columns

    # Create a stylized welcome message
    welcmsg = pyfiglet.figlet_format("Cipherion", font="slant").strip()
    
    # Center-align the separator and welcome message
    sep = "-" * terminal_width
    centered_welcmsg = welcmsg.center(terminal_width)
    centered_welcome_text = "Welcome to Cipherion!".center(terminal_width)
    centered_description = "A robust tool for encrypting and securely storing sensitive information.".center(terminal_width)

    # Display the welcome message with separators
    print(sep)
    print(centered_welcmsg)
    print(sep)
    print(centered_welcome_text)
    print(centered_description)
    print(sep)
