"""
Module Docstring
Docstrings: http://www.python.org/dev/peps/pep-0257/
"""

__author__ = 'Yannic Schneider (v@vendetta.ch)'
__copyright__ = 'Copyright (c) 20xx Yannic Schneider'
__license__ = 'WTFPL'
__vcs_id__ = '$Id$'
__version__ = '0.1' #Versioning: http://www.python.org/dev/peps/pep-0386/

#
## Code goes here.
#
import colorama
from colorama import Fore, Back, Style

LINE = '-' * 80
HEAD = '#' * 80

def SetTitle(nr):
    """ Testing Docstring"""
    print(Fore.MAGENTA + HEAD) 
    print('>> Cryptopals crypto challenge :: SET:%d ' % nr)                           
    print(Fore.MAGENTA + HEAD + Style.RESET_ALL) 


def ChallengeTitle(snr, cnr, subtitle=None):
    """ Testing Docstring"""
    sub = ' ' if subtitle == None else subtitle
    print(LINE) 
    if sub == ' ' : 
        print('>> Cryptopals :: SET:%d :: Challenge: %d' % (snr, cnr))
    else:
        print('>> Cryptopals :: SET:%d :: Challenge: %d :: Sub: %s' 
            % (snr, cnr, sub))   
    print(LINE + Style.RESET_ALL) 


def PrintResult(btest, bresult):
    """ Testing Docstring"""
    print(Fore.CYAN + LINE)
    print('>> Result bytes :: %s' % bresult)
    check = True if btest == bresult else False 
    if check:
        print(Fore.GREEN + '>> Result check ::  %s' % 'CORRECT' 
            + Style.RESET_ALL)  
    else:
        print(Fore.RED + '>> Result check ::  %s' % 'WRONG' 
            + Style.RESET_ALL)                           
