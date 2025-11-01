import os
import platform

def clear_screen():
    # Windows
    if platform.system() == 'Windows':
        os.system('cls')
    # macOS / Linux / Unix
    else:
        os.system('clear')