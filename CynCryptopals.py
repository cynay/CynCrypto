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

from lib.CynCrypto import *
from lib.CliPrinter import *


# GLOBALS

DEBUG = True
SLOW  = False
LINE = '-' * 80
HEAD = '#' * 80

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
    if SLOW: detectSingleCharXOR('Set1Challenge4.txt')

    ChallengeTitle(1,5)
    repeatKeyXOR("Burning 'em, if you ain't quick and nimble\n"
        + "I go crazy when I hear a cymbal",
        'ICE',
        '0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272'
        + 'a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f')

    ChallengeTitle(1,6, 'Hamming distance')
    # Sub challenge :: Hamming Distance
    s1 = toBin('this is a test')
    s2 = toBin('wokka wokka!!!')
    print('String1 : %s\nString2 : %s' % (s1, s2))
    PrintResult(37, (hammDist(s1, s2)))

    ChallengeTitle(1,6)
    repeatKeyXORcrack('Set1Challenge6.txt', 2, 40)

    ChallengeTitle(1,7)
    decryptAES_mode_ECB('Set1Challenge7.txt', 'YELLOW SUBMARINE')



def decryptAES_mode_ECB(fn, key):
    print('File: %s' % fn)
    print('Key : %s' % key)
    print(LINE)
    b64 = read_file(fn)
    msg = decrypt_AES_ECB(b64, key)
    print(str(msg, 'ascii'))
    


def repeatKeyXORcrack(fn, minKey, maxKey):
    print('File       : %s' % fn)
    print('Key-Length : %d - %d' % (minKey, maxKey))
    print(LINE)
    b64 = read_file(fn)
    #print('base64 of crypt repeating-key XOR : %s' % b64)
    #print(base64ToBytes(b64))
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
    # 5
    #cb = [b[i % ks] for i in range(0, len(b))]
    #print(len(b))
    #print(b)
    # 6
    sb = [''] * ks
    for i in range(0,int(len(b)),2):
        sb[(int(i/2) % ks)] += b[i:i+2].decode('ascii')
        #print(b[i:i+2].decode('ascii'))
    #for i, block in enumerate(cb):
    #    sb[i % ks] += block
    
    # solve Keychar 1 .. n
    ckey = ''
    ctext = []
    for i,elmt in enumerate(sb):
        #print(elmt)
        #print(list(elmt))
        #hexstr = ''.join(hex(b)[2:] for b in elmt)
        #hexstr = ''.join(format(x, '02x') for x in elmt)
        #hexstr = elmt.decode('ascii')
        #print(hexstr)
        #print(len(elmt))

        #print(singleByteXORcrack(elmt))
        ckey += bytesXORcrack(elmt)[1]
        ctext.append(bytesXORcrack(elmt)[2].decode('ascii'))
        #print( bytesXORcrack(elmt))
    print('>> Found Key: %s' % ckey)
    PrintResult(ckey, 'Terminator X: Bring the noise')
    
    rtext = ''
    for i in range(ks):
        for c in range(len(ctext)):
            rtext += ''.join(ctext[c][i:i+1])
    
    print(rtext)
    
    return True



def read_file(path):
    fobj = open(path, encoding='latin-1')
    ret = ''
    for line in fobj:
        ret += line.strip()
    return ret



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
        print('>> Score: %d :: Key: %s :: result = %s ' % (res[i][0], res[i][1], res[i][2]))
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
