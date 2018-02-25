import unittest
import sys
from master import *
import time
import datetime
testCase = 51000

bug = [0, ]
debugV = 0


def debug(s):
    global debugV
    print(str(s)  + " debug information " + str(debugV))
    debugV = debugV + 1


def setup(numServers):

   for i in range(numServers):
      joinServer(i)
      time.sleep(0.05)
      joinClient(i, i)




c = [randint(0, 4) for i in range(400)]
key = [randint(0, 2000)for i in range(400)]
value = [randint(0, 100)for i in range(400)]

# setup(5)
#
# for i in range(1):
#     print(datetime.datetime.now())
#     for j in range(40):
#         put(c[i*40+j], key[i*40+j], value[i*40+j])
#     stabilize()
#     print("finish ", i)



if testCase == 0:
    setup(3)
    put(0, 'x', 0)
    breakConnection(0, 0)
    createConnection(0, 1)
    time.sleep(0.05)
    put(0, 'x', 1)
    print (get(0, 'x'))
    breakConnection(0, 1)
    createConnection(0, 0)
    time.sleep(0.05)
    print (get(0, 'x'))

    print("finished")

#################################################
elif testCase == 1:
    print ("---[TEST 1] should output 0 1 1 1 4 ERR_DEP---")
    setup(2)
    put(0,"x", 0)
    put(1,"x", 1)
    put(0,"y", 2)
    time.sleep(0.05)
    put(1,"y", 3)
    get(0, "x")  # 0
    get(1, "x")  # 1
    printStore(0)
    stabilize()
    time.sleep(0.1)
    printStore(0)
    printStore(1)
    get(0, "x")  # 1
    get(1, "x")  # 1
    ## critical
    put(0,"x", 4)
    time.sleep(0.05)
    get(0, "x")  # 4
    time.sleep(0.05)
    get(0, "x")  # ERR_DEP
    printStore(1)
    print("finished")

##################################################
elif testCase == 2:
    # 1 s, 2 c
    print ("---[TEST 2] should output 0 1 3 4---")
    joinServer(0)
    joinServer(1)
    connectServers(0, 1)
    time.sleep(0.05)
    joinClient(0, 0)
    joinClient(1, 0)
    time.sleep(0.05)
    put(0,"x", 0)
    print(get(1, "x"))  # 0
    put(1,"x", 1)
    put(0,"x", 2)
    put(0,"x", 3)
    print(get(1, "x"))  # 1 !!! really important
    stabilize()
    print(get(1, "x"))  # 3
    put(0,"x", 4)
    print(get(0, "x")) # 4
    print("finished")
###################################################
elif testCase == 3:
    print ("---[TEST 3] should output ERR_DEP ERR_DEP 2---")
    #breakservers
    joinServer(0)
    time.sleep(0.05)
    joinServer(1)
    time.sleep(0.05)
    joinServer(2)
    time.sleep(0.05)
    joinServer(3)
    time.sleep(0.05)
    joinServer(4)
    time.sleep(0.05)
    joinClient(0, 0)
    time.sleep(0.05)
    put(0,"x", 0)
    #connectServers(0, 1)
    createConnection(0, 1) # c0 with s1
    time.sleep(0.05)
    put(0,"x", 2) # put x:2 in server 1
    createConnection(0, 0)
    time.sleep(0.05)
    get(0, "x") #  ERR_DEP
    #breakServers(0, 1)
    stabilize() # do nothing
    get(0, "x") #  ERR_DEP
    connectServers(0, 1)
    stabilize()
    get(0, "x") # 2

elif testCase == 31: # killserver
    setup(3)
    put (0, 0, 0)
    killServer(0)
    print(get(0,0))
    createConnection(0, 0)
    print(get(0, 0))

elif testCase == 41: # printStore
    setup(5)
    for j in range(5):
        for i in range(10):
            put(j, j * 10 + i, j * 10 + i)
        printStore(j)

elif testCase == 51: # Read your write
    setup(3)
    put(0, 'x', 0)
    breakConnection(0, 0)
    createConnection(0, 1)
    time.sleep(0.05)
    put(0, 'x', 1)
    print(get(0, 'x'))
    breakConnection(0, 1)
    createConnection(0, 0)
    time.sleep(0.05)
    print(get(0, 'x'))



elif testCase == 52: # Read your write 2, change
    print ('should output ERR_DEP ERR_DEP')
    setup(3)
    put(0, 'x', 0)
    put(1,'x', 1)
    breakConnection(0, 0)
    createConnection(0, 1)
    breakConnection(1,1)
    createConnection(1, 0)

    print(get(0, 'x'))
    print(get(1, 'x'))

elif testCase == 61: # test partition # break
    setup(5)
    for j in range(5):
        for i in range(10):
            put(j, 'x', j*10+i)
    #breakServers(2, 3) # ****
    stabilize()
    time.sleep(2)
    for i in range (5):
        printStore(i)
        #print get(i, 'x')

elif testCase ==8: # 1 server, 2 client
    setup(3)
    breakConnection(1,1)
    createConnection(1, 0)
    put(1, 'x', 1)
    put(0, 'x', 2)
    put(0, 'x', 3)
    print(get(0, 'x')) # 3
    print(get(1, 'x')) # 3
    stabilize()
    print(get(1, 'x')) # 3


elif testCase == 9:
    setup(3)
    for i in range(100):
        put(0, 'x', i)
    for i in range(10):
        put(1, 'x', 100+i)
    breakConnection(1, 1)
    createConnection(1, 0)
    print(get(1, 'x')) # ERR_DEP

    breakConnection(0, 0)
    createConnection(0, 1)
    print(get(0, 'x'))  # ERR_DEP

elif testCase == 10:  # 1 key ---- test time
    setup(5)
    start = time.time()
    for j in range(5):
        for i in range(10):
            put(j, 'x', j*10+i)
    end = time.time()
    putTime = (end - start)
    start = time.time()
    stabilize()

    end = time.time()
    stableTime = (end - start)
    start = time.time()
    for j in range(5):
        for i in range(10):
            get(j, 'x')
    end = time.time()
    getTime = (end - start)
    print('[only 1 key] put: ', putTime/50.0, ', get: ', getTime/50.0,  ', stable: ', stableTime)

    start = time.time()
    for j in range(5):
        for i in range(10):
            put(j, j * 10 + i, j * 10 + i)
    end = time.time()
    print('1')
    putTime = (end - start)
    start = time.time()


    stabilize()

    end = time.time()

    print('2')
    stableTime = (end - start)
    start = time.time()
    for j in range(5):
        for i in range(10):
            get(j, str(j * 10 + i))
    end = time.time()
    getTime = (end - start)
    print('3')
    print('[many keys] put: ', putTime/50.0, ', get: ', getTime/50.0,  ', stable: ', stableTime)
elif testCase == 11:  # 1 key ---- test time
    setup(5)

    for j in range(5):
        for i in range(10):
            put(j, 'x', j*10+i)

    stabilize()


    for j in range(5):
        for i in range(10):
            get(j, 'x')

    for j in range(5):
        for i in range(10):
            put(j, j * 10 + i, j * 10 + i)

    stabilize()


elif testCase == 100:
    numServer = 5
    setup(numServer)
    keys = list(string.ascii_lowercase)
    gt = [[None] * len(keys) for i in range(numServer)] # ground truth
    for i in xrange(10):
        for j in range(numServer):
            kId, v = genPair()
            gt[j][kId] = v
            put(j, keys[kId], v)

    for i in range(len(keys)):
        for j in range(numServer):
            real = gt[j][i] if gt[j][i]!= None else 'ERR_KEY'


