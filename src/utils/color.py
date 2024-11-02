from colorama import init, Fore, Style

init(autoreset=True)

colors = {
    '[INFO]': Fore.YELLOW,
    '[SUCCESS]': Fore.LIGHTGREEN_EX,
    '[FAIL]': Fore.RED,
    '[INPUT]': Fore.LIGHTBLUE_EX,
}

def color(tag, message, newline=False):
    newtag = colors.get(tag, Fore.WHITE) + tag + Style.RESET_ALL
    
    if newline:
        return f"\n{newtag} {message}"
    
    return f"{newtag} {message}"
