#!/usr/bin/python3
# -*- coding: ascii -*-

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

from lib.CynCrypto import *
from lib.CliPrinter import *


# GLOBALS

SLOW = True
LINE = '----------------------------------------------------------------------'

def __main__():
    """ Testing Docstring"""
    SetTitle(1)
    ChallengeTitle(1,1)
    convertHexToBase64(
        '49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d',
        'SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t')

    ChallengeTitle(1,2)
    fixedXOR('1c0111001f010100061a024b53535009181c',
        '686974207468652062756c6c277320657965',
        '746865206b696420646f6e277420706c6179')
    
    ChallengeTitle(1,3)
    singleByteXORcrack('1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736')

    ChallengeTitle(1,4)
    detectSingleCharXOR('Set1Challenge4.txt')



def detectSingleCharXOR(fn):
    top = 5
    print('Input  : %s' % fn)
    print(LINE)
    fobj = open(fn, encoding='latin-1')
    scores = []
    for line in fobj:
        bline = toHex(line[:-1])
        llen = len(bline)
        scores.append(singleXORcrack(bline, llen, maxp=1, doPrint=False))

    res = sorted(scores, key=lambda x: x[0], reverse=True)                         
                                                                                   
    print('>> Detect single char XOR crack :: top %d results :' % top)             
    best = b''                                                                     
    for i in range(top):                                                           
        if i == 0: best = res[i]                         
        print('>> Score: %d :: Key: %s :: result = %s ' % (res[i][0], res[i][1], res[i][2]))
    PrintResult(res[0][2], res[0][2])


def singleByteXORcrack(instr):
    print('Input  : %s' % instr)
    inhex = toHex(instr)
    inlen = len(inhex)
    print(line)
    res = singleXORcrack(inhex, inlen, maxp=5, doPrint=True)
    print(line)
    print('>> Best result: %s' % res[2])
    # Result check is cheated because we dont have an answer from the challenge
    PrintResult(res[2], res[2])



def fixedXOR(instr, bxor, test):
    print('Input  : %s' % instr)
    print('XORstr : %s' % bxor)
    print('Test   : %s' % test)
    inhex = toHex(instr)
    xorhex = toHex(bxor)
    testhex = toHex(test)
    res = (bXOR(inhex, xorhex))
    PrintResult(testhex, res)



def convertHexToBase64(instr, test):
    print('Input : %s' % instr)
    print('Test  : %s' % test)
    res = hexToBase64(instr)
    btest = bytes(test, 'ascii')
    PrintResult(btest, res)



if __name__=='__main__':
    __main__()
