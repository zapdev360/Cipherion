import pyfiglet
import shutil

def welcome():
    # Get the terminal width to make the separator dynamic
    terminal_width = shutil.get_terminal_size().columns
    sep = "-" * terminal_width

    # Create a stylized welcome message
    welcmsg = pyfiglet.figlet_format("Cipherion", font="slant")

    # Display the welcome message with separators
    print(sep)
    print(welcmsg)
    print(sep)
    print("Welcome to Cipherion!")
    print("A robust tool for encrypting and securely storing sensitive information.")
    print(sep)

# Call the welcome function
if __name__ == "__main__":
    welcome()
