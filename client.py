from copy import deepcopy
import random
import numpy as np
import math
import socket
import threading as th
import sys
import os

fin = open("config.txt", "r")
nextLine = fin.readline()
enctype = nextLine
nextLine = fin.readline()
encseed = nextLine
if(enctype[0] == "b" and enctype[1] == "b" and enctype[2] == "s"):
    encseedint = int(encseed)
else:
    encseedinttemp = np.array([])
    encseedarray = encseed.split()
    for node in encseedarray:
        encseedinttemp = np.append(encseedinttemp, int(node))
    encseedint = encseedinttemp.astype(int)

def solitaire(pakli, iteration):#53assal van jelolve a feher joker, 54 a fekete, erteke a feketenek 54bol 53 legyen a vegen. 
  #iteration szam azert van hogy [0,255] lehessen a visszateritett ertek, nem csak 52ig
  result = 0
  paklilen = len(pakli)
  for i in range(0, iteration):
    whitejokerindex = -1
    for i in range(0, paklilen):
      if(pakli[i] == 53):
        whitejokerindex = i
        break
    if(whitejokerindex == (paklilen - 1)):
      for j in range(paklilen-1, 1, -1):
        pakli[j] = pakli[j-1]
      pakli[1] = 53
    else:
      pakli[whitejokerindex] = pakli[whitejokerindex+1]
      pakli[whitejokerindex+1] = 53

    #print("a utan")
    #print(pakli)

    blackjokerindex = -1
    for i in range(0, paklilen):
      if(pakli[i] == 54):
        blackjokerindex = i
        break
    if(blackjokerindex == (paklilen - 1)):
      for j in range(paklilen-1, 2, -1):
        pakli[j] = pakli[j-1]
      pakli[2] = 54
    elif(blackjokerindex == (paklilen - 2)):
      for j in range(paklilen-2, 1, -1):
        pakli[j] = pakli[j-1]
      pakli[1] = 54

    #print("b utan")
    #print(pakli)

    firstjokerindex = -1
    secondjokerindex = -1
    for i in range(0, paklilen):
      if(pakli[i] == 53 or pakli[i] == 54):
        if(firstjokerindex == -1):
          firstjokerindex = i
        else:
          secondjokerindex = i
          break
    temppakli = np.array([])
    for i in range(secondjokerindex+1, paklilen):
      temppakli = np.append(temppakli, pakli[i])
    for i in range(firstjokerindex, secondjokerindex+1):
      temppakli = np.append(temppakli, pakli[i])
    for i in range(0, firstjokerindex):
      temppakli = np.append(temppakli, pakli[i])
    pakli = temppakli.astype(int)

    #print("c utan")
    #print(pakli)

    temppakli2 = np.array([])
    lastcardvalue = pakli[paklilen-1]

    if(lastcardvalue == 54):
      lastcardvalue = 53
    for i in range(lastcardvalue, paklilen-1):
      temppakli2 = np.append(temppakli2, pakli[i])
    for i in range(0, lastcardvalue):
      temppakli2 = np.append(temppakli2, pakli[i])
    temppakli2 = np.append(temppakli2, pakli[paklilen-1])
    pakli = temppakli2.astype(int)

    #print("d utan")
    #print(pakli)

    returnvalue = -1
    firstcardvalue = pakli[0]
    if(firstcardvalue == 54):
      firstcardvalue = 53
    keyelem = pakli[firstcardvalue]
    if(keyelem == 53 or keyelem==54):
      returnvalue, dumppakli = solitaire(pakli, 1)
    else:
      returnvalue = keyelem
    
    result = result + returnvalue
  
  result255 = result % 256
  return (result255, pakli) 

def bbs(s):
  #svalue = ord(s)#if input is string
  svalue = s
  p = 47
  q = 71
  n = p * q
  xs = np.array([])
  zs = np.array([])
  x0 = (svalue**2) % n
  xlast = x0
  xs = np.append(xs,x0)
  z0 = x0 % 2
  zs = np.append(zs, z0)
  for i in range(0,7):
    xi = (xlast**2) % n
    xs = np.append(xs, xi)
    zi = xi % 2
    zs = np.append(zs, zi)
    xlast = xi
  xsint = xs.astype(int)
  zsint = zs.astype(int)
  zslen = len(zsint)
  result = 0
  for i in range(0, zslen):
    result = result + (zsint[i] * (2 ** (zslen-1-i)))
  return result

def decodestream(func, seed, message):
  message = str(message, 'utf-8')
  encoded = np.array([])
  if(func == bbs):
    bbsnext = seed
    bbsres = -1
    for char in message:
      bbsres = bbs(bbsnext)
      encoded = np.append(encoded, bbsres)
      bbsnext = bbsres
    encodedint = encoded.astype(int)
    seedascii = np.array([])
    for char in message:
      seedascii = np.append(seedascii, ord(char))
    seedint = seedascii.astype(int)
    xorresult = np.array([])
    encodedlen = len(encodedint)
    for i in range(0, encodedlen):
      xori = seedint[i] ^ encodedint[i]
      xorresult = np.append(xorresult, xori)
    xorresultint = xorresult.astype(int)
    #print(seedint)
    #print(encodedint)
    #return xorresultint
    asciiresult = ""
    for node in xorresultint:
      asciichar = chr(node)
      #print("decode", node, asciichar)
      asciiresult += asciichar
    bytearrayresult = bytearray(asciiresult, 'utf-8')
    return bytearrayresult

  elif(func == solitaire):
    ujpakli = seed
    for char in message:
      solitairenumber, ujpakli = solitaire(ujpakli, 8)
      encoded = np.append(encoded, solitairenumber)
    encodedint = encoded.astype(int)
    seedascii = np.array([])
    #print(encodedint)
    for char in message:
      seedascii = np.append(seedascii, ord(char))
    seedint = seedascii.astype(int)
    xorresult = np.array([])
    encodedlen = len(encodedint)
    for i in range(0, encodedlen):
      xori = seedint[i] ^ encodedint[i]
      xorresult = np.append(xorresult, xori)
    xorresultint = xorresult.astype(int)
    #print(seedint)
    #print(encodedint)
    #return xorresultint
    asciiresult = ""
    for node in xorresultint:
      asciichar = chr(node)
      #print("decode", node, asciichar)
      asciiresult += asciichar
    bytearrayresult = bytearray(asciiresult, 'utf-8')
    return bytearrayresult

def incserver(mySocket: socket):
    while True:
        if(enctype[0] == "b"):
            mess = decodestream(bbs, encseedint, mySocket.recv(1024))
        else:
            fin2 = open("decodeseed.txt", "r")
            nextLine2 = fin2.readline()
            decseed = nextLine2
            encseedinttemp2 = np.array([])
            encseedarray2 = decseed.split()
            for node in encseedarray2:
                encseedinttemp2 = np.append(encseedinttemp2, int(node))
            encseedintfromfile = encseedinttemp2.astype(int)
            mess = decodestream(solitaire, encseedintfromfile, mySocket.recv(1024))
        strmess = str(mess, 'utf-8')
        print(strmess)

def outserver(mySocket: socket):
    mySocket.send((sys.argv[1].encode()))
    print("Type what you want to do")
    print("send - send a message to a specific user")
    print("exit - close connection with server")
    while True:
        print("$ ", end="")
        servertask = input()
        mySocket.send(servertask.encode())
        if servertask == "exit":
            mySocket.close()
            os._exit(0)
        elif servertask == "send":
            usernameinput = input("$ target user: ")
            mySocket.send(usernameinput.encode())
            messageinput = input("$ message to send: ")
            mySocket.send(messageinput.encode())

mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mySocket.connect(("localhost", 1234))
threadinc = th.Thread(target=incserver, args=(mySocket,))
threadinc.start()
threadout = th.Thread(target=outserver, args=(mySocket,))
threadout.start()