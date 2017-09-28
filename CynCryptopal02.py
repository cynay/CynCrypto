#!/usr/bin/python3
# -*- coding: ascii -*-

"""
Module Docstring
Docstrings: http://www.python.org/dev/peps/pep-0257/
"""

__author__ = 'Yannic Schneider (v@vendetta.ch)'
__copyright__ = 'Copyright (c) 2017 Yannic Schneider'
__license__ = 'WTFPL'
__vcs_id__ = '$Id$'
__version__ = '0.1' #Versioning: http://www.python.org/dev/peps/pep-0386/

#
## Code goes here.
#
from lib.CynLogger import *
from lib.CynCrypto import *
from lib.CliPrinter import *
from lib.CynUtil import *


# GLOBALS
APP_NAME    = 'CynCrypto.'
DEBUG       = True
SLOW        = False
LINE        = '-' * 80
HEAD        = '#' * 80

def __main__():
    """ Testing Docstring"""
    setup_logging(app_name = APP_NAME)
    log = logging.getLogger(APP_NAME + __name__)

    SetTitle(2)
    ChallengeTitle(2,1)
    res = pkcs7('YELLOW SUBMARINE', 20)
    PrintResult(b'YELLOW SUBMARINE\x04\x04\x04\x04', res)




if __name__=='__main__':
    __main__()
