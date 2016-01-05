import os
import sys
from there_application import which

def virtualenv_check():
    print('\033[92m Comprobando si esta instalado VIRTUALENV\033[0m')
    if which('virtualenv') == None:
        print('\033[91m  *  Virtualenv no esta instalado. Instalalo para poder seguir\033[0m')
        sys.exit(0)
    else:
        print('\033[92m  * Virtualenv esta instalado\033[0m')
        sys.exit(1)
