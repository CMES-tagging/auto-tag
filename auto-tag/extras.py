import os

# clear screen for Windows, Mac, Linux OS
def clear():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')
