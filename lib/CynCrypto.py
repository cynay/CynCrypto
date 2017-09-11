#!/usr/bin/env python
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
import string
import codecs
import base64
import binascii
import distance

# GLOBALS

ALPHA_LOWER = 'abcdefghijklmnopqrstuvwxyz'
ALPHA_UPPER = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
ALPHA_PRINT = string.printable

ALPHA_EN_MOST_UPPER = 'ETAOIN SHRDLU'
ALPHA_EN_MOST_LOWER = 'etaoin shrdlu'
ALPHA_EN_MOST = ALPHA_EN_MOST_LOWER + ALPHA_EN_MOST_UPPER

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


# Conversions

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
            + wordScoreEN(results[key]))
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
