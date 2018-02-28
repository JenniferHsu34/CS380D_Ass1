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
        joinClient(i+5, i)


testCase = 'performance'
# here you can put: eventualConsistency read-your-write monotonicReads
# joinServer killServer printStore joinClient breakConnection createConnection stabilize put get
if testCase =='eventualConsistency':
    print ('test [eventual Consistency] property ')
    numServer = 5
    numClient = 5
    setup(numServer)
    keys = list(string.ascii_lowercase)

    err = 0
    gt = [['ERR_KEY'] * len(keys) for i in range(numClient)]  # ground truth
    for i in xrange(10):
        for j in range(numClient):
            kId, v = genPair(len(keys), 10000)
            gt[j][kId] = v
            # print 'put ', j, keys[kId], v
            put(j+5, keys[kId], v)

            get(j+5, keys[kId])
    stabilize()
    # after stabilize, for each key, check if the values getting from all clients are the same
    for i in range(len(keys)):
        values = ['None'] * numClient
        for j in range(numClient):
            values[j] = get(j+5, keys[i])
        for k in range(numClient):
            if values[k] != values[(k + 1) % numClient]:
                err += 1
            print('get: ', values[k], ', ground truth is: ', values[(k + 1) % numClient])


    print ('Get ', err, ' mismatches. 0 err means achieve eventually consistency')
    os._exit(1)

elif testCase == 'read-your-write':
    print ('test [read-your-write] property ')
    setup(3)
    for i in range(100):
        put(5, 'x', i)

    for i in range(10):
        put(6, 'x', 100 + i)

    breakConnection(6, 1)
    createConnection(6, 0)
    print(get(6, 'x'))  # 99

    breakConnection(5, 0)
    createConnection(5, 1)
    print(get(5, 'x'))  # ERR_DEP
    stabilize()
    print(get(6, 'x'))  # 99
    print(get(5, 'x'))  # 99
    print ('we have c0 conntects to s0 and c1 connects to s1 intially and put some values to key x. Then, we switch connection and check if client could get latest write(or output ERR_DEP')
    os._exit(1)

elif testCase == 'monotonicReads':  # Test Monotonic Reads.
    print ('test [Monotonic Reads] property ')
    joinServer(4)
    joinServer(3)
    joinClient(5, 3)
    joinClient(7, 4)
    put(5, 'x', 0)
    put(7, 'x', 1)
    joinClient(8, 3)
    print (get(8, 'x'))
    breakConnection(8, 3)
    createConnection(8, 4)
    print (get(8, 'x'))
    # time.sleep(0.5)
    breakConnection(8, 4)
    createConnection(8, 3)
    print (get(8, 'x'), ' this value should be ERR_DEP because it switch to previous server')  # get ERR_DEP
    print 'done Monotonic Reads check'
    os._exit(1)

elif testCase == 'performance':  # test performance ----
    setup(5)
    start = time.time()
    for j in range(5):
        for i in range(100):
            put(j+5, 'x', j * 100 + i)
    end = time.time()
    putTime = (end - start)
    start = time.time()
    stabilize()

    end = time.time()
    stableTime = (end - start)
    start = time.time()
    for j in range(5):
        for i in range(100):
            get(j+5, 'x')
    end = time.time()
    getTime = (end - start)
    print('[only 1 key] put: ', putTime / 500.0, ', get: ', getTime / 500.0, ', stable: ', stableTime)
    totalTemp = putTime+getTime
    start = time.time()
    for j in range(5):
        for i in range(100):
            put(j+5, j * 100 + i, j * 100 + i)
    end = time.time()

    putTime = (end - start)
    start = time.time()

    stabilize()

    end = time.time()


    stableTime = (end - start)
    start = time.time()
    for j in range(5):
        for i in range(100):
            get(j+5, str(j * 100 + i))
    end = time.time()
    getTime = (end - start)
    totalTemp += putTime + getTime
    print('[many keys] put: ', putTime / 500.0, ', get: ', getTime / 500.0, ', stable: ', stableTime)
    print ('Per second perform', 2000/totalTemp/1.0, 'instructions')
    os._exit(1)

elif testCase == 'joinServer': # joinServer
    print (' test joinServer. perform basic commands combining with stabilize and printStore to see if we join server correctly')
    # breakservers
    joinServer(0)
    joinServer(1)
    joinServer(2)
    joinServer(3)
    joinServer(4)
    joinClient(5, 0)
    put(5, "x", 0)
    createConnection(0, 1)
    createConnection(5, 1)  # c0 with s1

    put(5, "x", 2)  # put x:2 in server 1
    createConnection(5, 0)

    print (get(5, "x"))  # ERR_DEP
    # breakServers(0, 1)
    stabilize()  # do nothing
    print (get(5, "x"))  # 2
    createConnection(0, 1)
    stabilize()
    print (get(5, "x"))  # 2
    print ('finish testing')
    for i in range(5):
        printStore(i)
    os._exit(1)
elif testCase == 'killServer':
    setup(3)
    put(5, 0, 0)
    killServer(0)
    print(get(5, 0))
    createConnection(5, 0)
    print(get(5, 0))
    print ('Finish test killServer. client 5 only connect to server0. Once server 0 got killed, we cant get any data from client 5')
    os._exit(1)

elif testCase == 'printStore':  # printStore
    print ('perform basic prinStore operation')
    setup(5)
    for j in range(5):
        for i in range(10):
            put(j+5, j * 10 + i, j * 10 + i)
        printStore(j)
    os._exit(1)
elif testCase == 'joinClient':

    print ("test [joinClient] API. ")
    joinServer(0)
    joinServer(1)
    time.sleep(0.05)
    joinClient(0, 0)
    joinClient(1, 0)
    time.sleep(0.05)
    put(0, "x", 0)
    print(get(1, "x"))  # 0
    put(1, "x", 1)
    put(0, "x", 2)
    put(0, "x", 3)
    print(get(1, "x"))  # 3
    stabilize()
    print(get(1, "x"))  # 3
    put(0, "x", 4)
    print(get(0, "x"))  # 4
    print("finished")
    os._exit(1)

elif testCase == 'breackConnection':  # test breackConnection/Connection between servers
    print ('test [breackConnection] API. ')
    numSer = 2
    setup(numSer)
    for j in range(numSer):
        for i in range(10):
            put(j+5, 'x', j * 10 + i)
    breakConnection(0, 1)  #
    stabilize()

    print ('We break the connection between s0 and s1. since server 0 and 1 do not connect. After stabilizing they do not have consistent view')
    for i in range(numSer):
        printStore(i)

    createConnection(0, 1)
    stabilize()
    print ('We re-create connection between server 0 and 1. After stabilizing they now have consistent view')
    for i in range(numSer):
        printStore(i)
    os._exit(1)

elif testCase == 'createConnection':  # 1 server, 2 client
    print ('test [createConnection] API. ')
    numSer = 3
    setup(numSer)
    for j in range(numSer):
        for i in range(10):
            put(j+5, 'y', j * 10 + i)
    breakConnection(0, 1)  #
    stabilize()

    print ('since server 0 and 1 do not connect. After stabilizing they do not have consistent view')
    for i in range(numSer):
        printStore(i)

    createConnection(0, 1)
    stabilize()
    print ('We re-create connection between server 0 and 1. After stabilizing they now have consistent view')
    for i in range(numSer):
        printStore(i)
    os._exit(1)
elif testCase == 'stabilize':

    numSer = 5
    setup(numSer)
    for j in range(numSer):
        for i in range(10):
            put(j+5, 'x', j * 10 + i)
    print ('Before stabilize, each server has different view')
    for i in range(numSer):
        printStore(i)

    stabilize()

    print ('After stabilize, each server has same view')
    for i in range(numSer):
        printStore(i)
        # print get(i, 'x')
    os._exit(1)

elif testCase == 'put':
    print ('test [put] API')
    setup(2)
    put(5, 'x', 0)
    printStore(0)
    os._exit(1)

elif testCase == 'get':
    print ('test normal [get] API')
    setup(2)
    put(5, 'x', 0)

