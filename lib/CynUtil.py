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

def read_file(path):
    """Read a file and return as string object"""
    return open(path, encoding='latin-1')

def read_file_strip(path):
    """Read a file and strip newlines so the result is on one line"""
    fobj = open(path, encoding='latin-1')
    ret  = ''
    for line in fobj:
        ret += line.strip()
    return ret

