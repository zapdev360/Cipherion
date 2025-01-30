import sys
import readchar

def maskpass(prompt):
    print(prompt, end="", flush=True)  
    pwd = ""
    while True:
        char = readchar.readchar() 

        if char == "\r" or char == "\n":  
            print()  
            break
        elif char == "\x7f" or char == "\b":
            if len(pwd) > 0:
                pwd = pwd[:-1]  
                sys.stdout.write("\b \b") 
                sys.stdout.flush()
        else:
            pwd += char
            sys.stdout.write("*")
            sys.stdout.flush()
    return pwd
