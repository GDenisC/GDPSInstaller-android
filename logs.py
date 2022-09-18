
from typing import Literal
from colorama import *
from const import DEBUG
init()

def log(message: str, *, error: Literal['LOG', 'WARN', 'ERROR'] = 'LOG') -> None:
    if DEBUG:
        if error == 'LOG':
            s = Fore.LIGHTCYAN_EX
        elif error == 'WARN':
            s = Fore.YELLOW
        elif error == 'ERROR':
            s = Fore.RED
        print(s+f'[{error}]'+Fore.RESET, message)

def loginput(message: str, *, error: Literal['LOG', 'WARN', 'ERROR'] = 'LOG') -> str:
    log(message, error=error)
    return input(' > ')
