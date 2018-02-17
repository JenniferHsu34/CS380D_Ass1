import unittest
import sys
from master import *
testCase =0

debugV = 0


def debug(s):
    global debugV
    print(str(s)  + " debug information " + str(debugV))
    debugV = debugV + 1

#set up servers with corresponding clients and make them fully connected
def setup(numServers):
    for i in range(numServers):
        joinServer(i)
        time.sleep(0.05)
        joinClient(i, i)

    for i in range(numServers):
        for j in range(numServers):
            if(i<j):
                connectServers(i,j)





if testCase == 0:
    setup(2)
    for i in range(100):
        put(0, str(i), i)
        put(1, "y", -i)
    stabilize()
    for i in range(100):
        put(0, str(i), 100+i)
        put(1, str(i),100-i )
    get(0, "x")  # 0
    get(1, "x")  # 1
    print("finished")

#################################################
elif testCase == 1:
    print ("---[TEST 1] should output 0 1 1 1 4 ERR_DEP---")
    setup(2)
    put(0,"x", 0)
    put(1,"x", 1)
    put(0,"y", 2)
    put(1,"y", 3)
    get(0, "x")  # 0
    get(1, "x")  # 1
    stabilize()
    get(0, "x")  # 1
    get(1, "x")  # 1
    ## critical
    put(0,"x", 4)

    time.sleep(0.05)
    get(0, "x")  # 4
    time.sleep(0.05)
    get(0, "x")  # ERR_DEP
    print("finished")

##################################################
elif testCase == 2:
    # 1 s, 2 c
    print ("---[TEST 2] should output 0 1 3 4---")
    joinServer(0)
    time.sleep(0.05)
    joinClient(0, 0)
    joinClient(1, 0)
    time.sleep(0.05)
    put(0,"x", 0)
    get(1, "x")  # 0
    put(1,"x", 1)
    put(0,"x", 2)
    put(0,"x", 3)
    get(1, "x")  # 1 !!! really important
    stabilize()
    get(1, "x")  # 3
    put(0,"x", 4)
    get(0, "x") # 4
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
else:
    # TESTING
    setup(3)


    print ('-----before stablize')
    debug(get(0, "x"))  # should get 2
    print ('get x from s1: (exp 1)')
    get(1, "x")  # should get 1
    stabilize()
    # time.sleep(1)
    print ('-----after stablize')
    get(1, "x")  # should get 1

