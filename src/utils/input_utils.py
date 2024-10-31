import sys
import readchar
def get_password(prompt):
    print(prompt, end="", flush=True)  
    password = ""
    while True:
        char = readchar.readchar() 

        if char == "\r" or char == "\n":  
            print()  
            break
        elif char == "\x7f" or char == "\b":  # works for all windows\linux\unix
            if len(password) > 0:
                password = password[:-1]  
                sys.stdout.write("\b \b") 
                sys.stdout.flush()
        else:
            password += char
            sys.stdout.write("*")  # Print asterisk for each typed character
            sys.stdout.flush()
    return password