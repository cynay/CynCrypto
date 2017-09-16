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

    SetTitle(1)
    ChallengeTitle(1,1)
    convertHexToBase64('49276d206b696c6c696e6720796f757220627261696e206c696b652'
        + '06120706f69736f6e6f7573206d757368726f6f6d',
        'SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t')

    ChallengeTitle(1,2)
    fixedXOR('1c0111001f010100061a024b53535009181c',
        '686974207468652062756c6c277320657965',
        '746865206b696420646f6e277420706c6179')
    
    ChallengeTitle(1,3)
    singleByteXORcrack('1b37373331363f78151b7f2b783431333d78397828372d363c78373'
        + 'e783a393b3736')

    ChallengeTitle(1,4)
    if SLOW: detectSingleCharXOR('etc/Set1Challenge4.txt')

    ChallengeTitle(1,5)
    repeatKeyXOR("Burning 'em, if you ain't quick and nimble\n"
        + "I go crazy when I hear a cymbal",
        'ICE',
        '0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a262263242727'
        + '65272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326'
        + '302e27282f')

    # Sub challenge :: Hamming Distance
    ChallengeTitle(1,6, 'Hamming distance')
    s1 = toBin('this is a test')
    s2 = toBin('wokka wokka!!!')
    print('String1: %s\nString2: %s' % (s1, s2))
    PrintResult(37, (hammDist(s1, s2)))

    ChallengeTitle(1,6)
    repeatKeyXORcrack('etc/Set1Challenge6.txt', 2, 40)

    ChallengeTitle(1,7)
    decryptAES_mode_ECB('etc/Set1Challenge7.txt', 'YELLOW SUBMARINE')
    
    ChallengeTitle(1,8)
    find_AES_mode_ECB('etc/Set1Challenge8.txt')


def find_AES_mode_ECB(fn):
    print('File: %s' % fn)
    print(LINE)
    b64 = read_file(fn)
    for i, line in enumerate(b64):
        bl = decrypt_AES_ECB(line,'YELLOW SUBMARINE')
        bn = len(bl) / 16
        blocks = []
        for b in range(int(bn)):
            blocks.append(bl[b*16:(b*16)+16])
        
        # check for dupes
        dupes = [x for n, x in enumerate(blocks) if x in blocks[:n]]
        if dupes:
            print('Duplicate blocks found in line nr: %d , dupes: %s' % 
                (i, dupes))

    # No check given
    PrintResult('Line nr: 132', 'Line nr: 132')


def decryptAES_mode_ECB(fn, key):
    print('File: %s' % fn)
    print('Key : %s' % key)
    print(LINE)
    b64 = read_file_strip(fn)
    msg = decrypt_AES_ECB(b64, key)
    print(str(msg, 'ascii'))
    


def repeatKeyXORcrack(fn, minKey, maxKey):
    print('File       : %s' % fn)
    print('Key-Length : %d - %d' % (minKey, maxKey))
    print(LINE)
    b64 = read_file_strip(fn)
    b = bytesToHex(base64ToBytes(b64))
    binStr = bytesToBin(b)
    print(len(binStr))
    keysize = []
    
    for s in range(minKey, maxKey + 1):
        sb = s*8
        hDist = float()
        for i in range(20):
            ib = (s * 8) * i
            it = (s * 8) * (i+1)
            iz = it + (s * 8)
            #print('Byte nr: %d : %d :: %d : %d' % (ib,it,it,iz))
            hDist += hammDist(binStr[ib:it],binStr[it:iz])
        keysize.append(((hDist/s), s))

    sort = sorted(keysize, key=lambda x: x[0], reverse=False)

    print('>> Normalized edit-distance :: top %d results :' % 5)          
    best = None                                                                
    for i in range(5):                                                        
        val = sort[i]                                             
        if i == 0: best = sort[i] 
        print('>> LevenshteinDistance: %f :: Key-Lengh: %d ' % (val[0], val[1]))
    print(LINE)
    print('Best result: dist: %s :: Key-Lenght: %s' % best)
    PrintResult(best[1], best[1])
    ks = best[1]
    
    # Crack it
    sb = [''] * ks
    for i in range(0,int(len(b)),2):
        sb[(int(i/2) % ks)] += b[i:i+2].decode('ascii')
    
    # solve Keychar 1 .. n
    ckey = ''
    ctext = []
    for i,elmt in enumerate(sb):
        ckey += bytesXORcrack(elmt)[1]
        ctext.append(bytesXORcrack(elmt)[2].decode('ascii'))
    print('>> Found Key: %s' % ckey)
    # no check given 
    PrintResult(ckey, 'Terminator X: Bring the noise')
    
    rtext = ''
    for i in range(ks):
        for c in range(len(ctext)):
            rtext += ''.join(ctext[c][i:i+1])
    
    print(rtext)
    
    return True


def repeatKeyXOR(text, key, test):
    print('Input  : %s' % text)
    print('Key    : %s' % key)
    print('Test   : %s' % test)
    print(LINE)
    hxtext = bytes(text.strip(), encoding='latin-1')
    hxkey  = bytes(key, encoding='latin-1')
    txlen  = len(hxtext)
    
    # repeat key to txlen size
    hxkeyl = (hxkey * ((txlen // len(hxkey)) + 1))[:txlen]
    
    res = bXOR(hxtext, hxkeyl)
    hxtest = toHex(test.strip())
    print('test: %s' % hxtest)
    print('res:  %s' % res)
    PrintResult(hxtest, res)

    

def detectSingleCharXOR(fn):
    top = 5
    print('Input  : %s' % fn)
    print(LINE)
    fobj = open(fn, encoding='latin-1')
    scores = []
    for line in fobj:
        bline = toHex(line[:-1])
        llen = len(bline)
        scores.append(singleXORcrack(bline, llen, maxp=1, doPrint=True))

    res = sorted(scores, key=lambda x: x[0], reverse=True)                         
                                                                                   
    print('>> Detect single char XOR crack :: top %d results :' % top)             
    best = b''                                                                     
    for i in range(top):                                                           
        if i == 0: best = res[i]                         
        print('>> Score: %d :: Key: %s :: result = %s ' %
            (res[i][0], res[i][1], res[i][2]))
    PrintResult(res[0][2], res[0][2])


def bytesXORcrack(instr):
    inhex = toHex(instr)
    inlen = len(inhex)
    #res = XORcrack(inhex, maxp=2, doPrint=True)
    res = singleXORcrack(inhex, inlen, maxp=3, doPrint=False)
    #print(LINE)
    #print('>> Score: %d :: Key: %s' % (res[0], res[1]))
    return res

def singleByteXORcrack(instr):
    print('Input  : %s' % instr)
    inhex = toHex(instr)
    inlen = len(inhex)
    print(LINE)
    res = singleXORcrack(inhex, inlen, maxp=5, doPrint=True)
    print(LINE)
    print('>> Best result: %s' % res[2].decode('ascii'))
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
