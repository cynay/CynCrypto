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
import string
import struct
import codecs
import base64
import binascii
import distance

from Crypto.Cipher import AES

# GLOBALS

ALPHA_LOWER = 'abcdefghijklmnopqrstuvwxyz'
ALPHA_UPPER = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
ALPHA_PRINT = string.printable

ALPHA_EN_MOST_UPPER = 'ETAOIN SHRDLU'
ALPHA_EN_MOST_LOWER = 'etaoin shrdlu'
ALPHA_EN_MOST       = ALPHA_EN_MOST_LOWER + ALPHA_EN_MOST_UPPER

ALPHA_DE_MOST_UPPER = 'ENISR ATDHU'
ALPHA_DE_MOST_LOWER = 'enisr atdhu'
ALPHA_DE_MOST       = ALPHA_DE_MOST_LOWER + ALPHA_DE_MOST_UPPER

WORDS_EN_MOST = ['the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'I', 
  'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at', 'this', 
  'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she', 'or', 'an', 
  'will', 'my', 'one', 'all', 'would', 'there', 'their', 'what', 'so', 'up', 
  'out', 'if', 'about', 'who', 'get', 'which', 'go', 'me', 'when', 'make', 
  'can', 'like', 'time', 'no', 'just', 'him', 'know', 'take', 'people', 'into',
  'year', 'your', 'good', 'some', 'could', 'them', 'see', 'other', 'than', 
  'then', 'now', 'look', 'only', 'come', 'its', 'over', 'think', 'also', 
  'back', 'after', 'use', 'two', 'how', 'our', 'work', 'first', 'well', 'way', 
  'even', 'new', 'want', 'because', 'any', 'these', 'give', 'day', 'most', 
  'us']

ALPHA_EN_FREQ = {
    'a': 12.702,
    'b': 1.492,
    'c': 2.782,
    'd': 4.253,
    'e': 12.702,
    'f': 2.228,
    'g': 2.015,
    'h': 6.094,
    'i': 6.966,
    'j': 0.153,
    'k': 0.772,
    'l': 4.025,
    'm': 2.406,
    'n': 6.749,
    'o': 7.507,
    'p': 1.929,
    'q': 0.095,
    'r': 5.987,
    's': 6.686,
    't': 15.978,
    'u': 1.183,
    'v': 0.824,
    'w': 5.497,
    'x': 0.045,
    'y': 0.763,
    'z': 0.045 }

ALPHA_DE_FREQ = {
    'a': 6.516,
    'b': 1.886,
    'c': 2.732,
    'd': 5.076,
    'e': 16.396,
    'f': 1.656,
    'g': 3.009,
    'h': 4.577,
    'i': 6.550,
    'j': 0.268,
    'k': 1.417,
    'l': 3.437,
    'm': 2.534,
    'n': 9.776,
    'o': 2.494,
    'p': 0.670,
    'q': 0.018,
    'r': 7.003,
    's': 7.270,
    't': 6.154,
    'u': 4.166,
    'v': 0.846,
    'w': 1.921,
    'x': 0.034,
    'y': 0.039,
    'z': 1.134 }

# Conversions with struct
# struct.pack(fmt, v1, v2, ...)
# Return a bytes object containing the values v1, v2, ... packed according to 
# the format string fmt. The arguments must match the values required by the 
# format exactly.

# struct.unpack(fmt, buffer)
# Unpack from the buffer buffer (presumably packed by pack(fmt, ...)) 
# according to the format string fmt. The result is a tuple even if it 
# contains exactly one item. The buffer’s size in bytes must match the size 
# required by the format, as reflected by calcsize().
def bToHexB2(b):
    return unpack('B',b)

def bToHexB(b):
    return binascii.hexlify(b)

def bToHexS(b):
    return binascii.hexlify(b).decode('ascii')



# Conversions old 

# String to ...
def toBin(input):
    return ''.join(format(ord(x), 'b').zfill(8) for x in input)


def toHex(input):
    return codecs.decode(input, 'hex')


def strXOR(input, xorStr):
    return int(input) ^ int(xorStr)


# Bytes to ...
def bytesToHex(b):
    return binascii.hexlify(b)


def bytesToAscii(b):
    # ToDo
    return b

def bytesToBin(b):
    binStr = ''
    for byte in range(0, len(b),2):
        #print('Byte: %s' % b[byte:byte + 2])
        binStr += bin(int(b[byte:byte+2], base=16))[2:].zfill(8)
        #print('Binary String: %s' % binStr)
    return binStr

# HEX to ...
def hexToBase64(hex):
    """ Testing Docstring"""
    return (binascii.b2a_base64(codecs.decode(hex,'hex')))[:-1]


# Base64 to ...
def base64ToHex(b64):
    return binascii.a2b_base64(b64)


def base64ToBytes(b64):
    return base64.b64decode(b64)

# XOR methods

def bXOR(b1,b2):
    res = bytearray()
    for b1, b2 in zip(b1, b2):
        res.append(b1 ^ b2)
    return bytes(res)


def XORcrack(b1, maxp=None, doPrint=None):
    top = 5 if maxp == None else maxp
    showPrint = False if doPrint == None else True
    inlen = len(b1)
    results = {}
    for i in range(127):
        char = chr(i) 
        b2 = bytes(char * inlen, 'ascii')
        results[char] = bXOR(b1, b2)
    
    scores = []
    for key in results:
        #print(results[key], file=open('out.txt', 'a'))
        scores.append((
            (mostLetterScoreEN(results[key]),
            + letterScoreEN(results[key])),
            key))

    res = sorted(scores, key=lambda x: x[0], reverse=True)

    if doPrint: print('>> Single XOR crack :: top %d results :' % top)
    best = b''
    for i in range(top):
        if i == 0: best = (res[i][0], res[i][1])
        #if doPrint: print('>> Score: %d :: Key: %s ' % (res[i][0], res[i][1] ))
    return best


def singleXORcrack(b1, inlen, maxp=None, doPrint=None):
    top = 5 if maxp == None else maxp
    showPrint = False if doPrint == None else True

    results = {}
    for i in range(127):
        char = chr(i) 
        b2 = bytes(char * inlen, 'ascii')
        results[char] = bXOR(b1, b2)
    

    scores = []
    for key in results:
        #print(results[key], file=open('out.txt', 'a'))
        scores.append((
            (letterScoreEN(results[key])
            + wordScoreEN(results[key])
            + mostLetterScoreEN(results[key]))
            , key))

    res = sorted(scores, key=lambda x: x[0], reverse=True)
    
    if doPrint: print('>> Single XOR crack :: top %d results :' % top)
    best = b''
    for i in range(top):
        decode = results[res[i][1]]
        if i == 0: best = (res[i][0], res[i][1], decode)
        if doPrint: print('>> Score: %d :: Key: %s :: result = %s ' % (res[i][0], res[i][1], decode))
    return best


# Analysis

def hammDist(in1, in2):
    diffs = 0                                                                   
    for ch1, ch2 in zip(in1, in2):                    
        if ch1 != ch2:                                                          
            diffs += 1                                                                            
    return diffs



def levenshteinDistance(in1, in2):
    return distance.levenshtein(in1, in2)



def hammingDistance(in1, in2):
    return distance.hamming(in1, in2)



def mostLetterScoreEN(inbytes):
    score = 0
    for c in inbytes:
        score += 13 if chr(c) == 'e' else 0
        score += 9 if chr(c) == 't' else 0
        score += 8 if chr(c) == 'a' else 0
        score += 7 if chr(c) == 'o' else 0
        score += 7 if chr(c) == 'i' else 0
        score += 6 if chr(c) == 'n' else 0
        
        score -= 6 if chr(c) == '#' else 0
        score -= 10 if chr(c) == ')' else 0
        score -= 10 if chr(c) == '+' else 0
        
    return score

 
def letterScoreEN(inbytes):
    score = 0
    for c in inbytes:
        #score += 5 if chr(c) in ALPHA_EN_MOST else 0
        score += 3 if chr(c) in ALPHA_LOWER else 0
        score += 2 if chr(c) in ALPHA_UPPER else 0
    
    return score


def wordScoreEN(inbytes):
    score = 0
    for word in inbytes.decode('latin-1').split(' '):
        score += 10 if word in WORDS_EN_MOST else 0
    
    return score


def decrypt_AES_ECB(b64, key):
    obj = AES.new(key, AES.MODE_ECB)
    b = base64.b64decode(b64)
    return obj.decrypt(b)


def pkcs7(txt, blocksize):
    pad = blocksize % len(txt)
    return txt.encode() + (b'\x04' * pad)
