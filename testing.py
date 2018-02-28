import unittest
import sys
from master import *
import time
import datetime
import string
import os

bug = [0, ]
debugV = 0


def genPair(krange, vrange):
    kid = randint(0, krange - 1)
    val = randint(0, vrange - 1)
    return kid, val


def debug(s):
    global debugV
    print(str(s) + " debug information " + str(debugV))
    debugV = debugV + 1


def setup(numServers):
    for i in range(numServers):
        joinServer(i)
        time.sleep(0.01)
        joinClient(i, i)


c = [randint(0, 4) for i in range(400)]
key = [randint(0, 2000) for i in range(400)]
value = [randint(0, 100) for i in range(400)]

# startTime = time.time()
# setup(5)
# for i in range(1):
#     for j in range(40):
#         put(c[i*40+j], key[i*40+j], value[i*40+j])
#     stabilize()
#     print("finish ", i)
#     put(0, "x", 1)
#     print(time.time()-startTime)


'''
setup(5)

for i in range(1):
    print(datetime.datetime.now())
    for j in range(40):
        put(c[i*40+j], key[i*40+j], value[i*40+j])
    stabilize()
    print("finish ", i)
'''
testCase = 83

for i in range(1):
    joinServer(0)
    joinServer(1)
    joinServer(2)
    joinServer(3)
    breakConnection(0,1)
    breakConnection(0,2)
    breakConnection(0,3)
    joinClient(5,0)
    joinClient(6,0)
    put(5,"x",1)
    get(6,"x")
    breakConnection(6,0)
    createConnection(6,2)
    print(get(5, "x"))
    createConnection(0,2)
    stabilize()
    put(6,"y",5)
    print(get(6, "x"))
    createConnection(6, 3)
    killServer(0)
    createConnection(5, 0)
    print(get(5, "x"))

    time.sleep(1)
    print(get(5, "x"))
    '''
    print(get(6,"x"))
    createConnection(6, 2)
    print(get(6, "x"))
    put(6,"x",2)
    print(get(6, "x"))
    print("Here")
    killServer(2)
    time.sleep(0.1)
    print("Here")
    stabilize()
    print("Here")
    print(get(5, "x"))
    print("Here")
    createConnection(0,1)
    stabilize()
    print("Here")
    print(get(5, "x"))
    '''
