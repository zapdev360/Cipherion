import pyfiglet
import shutil

def welcome():
    # Get the terminal width to make the separator dynamic
    terminal_width = shutil.get_terminal_size().columns

    # Create a stylized welcome message
    welcmsg = pyfiglet.figlet_format("Cipherion", font="slant").strip()
    
    # Split the welcome message into lines for proper centering
    welcmsg_lines = welcmsg.split('\n')
    centered_welcmsg = '\n'.join([line.center(terminal_width) for line in welcmsg_lines])
    
    # Center-align the separator and other texts
    sep = "-" * terminal_width
    centered_welcome_text = "Welcome to Cipherion!".center(terminal_width)
    centered_description = "A robust tool for encrypting and securely storing sensitive information.".center(terminal_width)

    # Display the welcome message with separators
    print(sep)
    print(centered_welcmsg)
    print(sep)
    print(centered_welcome_text)
    print(centered_description)
    print(sep)

# Note: The call to welcome() was removed from this script as it is controlled by the main execution flow in main.py
