import unittest
import sys
from master import *
testCase =5

debugV = 0


def debug(s):
    global debugV
    print(str(s)  + " debug information " + str(debugV))
    debugV = debugV + 1


if testCase == 0:
    joinServer(0)
    time.sleep(0.05)
    #time.sleep(1)
    joinClient(0, 0)

    put(0,"x", 0)
    breakConnection(0, 0) # c, s
    joinServer(1)
    time.sleep(0.05)
    createConnection(0, 1)
    put(0,"x", 1) # now, data should only send to server1
    get(0, "x") # 1
    breakConnection(0, 1)
    createConnection(0, 0) # now, c0 only connect to s0
    get(0, "x") # should output ERR_DEP
    createConnection(0, 1)
    stabilize()
    get(0, "x") # should get from s0? output 1
#################################################
elif testCase == 1:
    # 1 s, 2 c
    joinServer(0)
    joinClient(0, 0)
    joinClient(1, 1)
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
    get(0, "x")  # 4
    breakConnection(0, 0)
    get(0, "x")  # ERR_DEP

##################################################
elif testCase == 2:
    # 1 s, 2 c

    joinServer(0)
    joinClient(0, 0)
    joinClient(1, 1)
    put(0,"x", 0)
    get(1, "x")  # 0
    put(1,"x", 1)
    put(0,"x", 2)
    put(0,"x", 3)
    get(1, "x")  # 1 !!! really important
    stabilize()
    get(1, "x")  # 3
    put(0,"x", 4)

###################################################
elif testCase == 3:
    #breakservers
    joinServer(0)
    joinServer(1)
    joinServer(2)
    joinServer(3)
    joinServer(4)
    joinClient(0, 0)
    put(0,"x", 0)
    createConnection(0, 1) # c0 with s1
    breakConnection(0, 0)

    put(0,"x", 2) # put x:2 in server 1
    breakConnection(0, 1) # break server 1
    get(0, "x") #  ERR_DEP
    breakservers(0, 1)
    stabilize() # do nothing
    get(0, "x") #  ERR_DEP
    connectServers(0, 1)
    stabilize()
    get(0, "x") # 2
else:
    # TESTING
    debug("ffff")

    debug("fffwwwww")
    joinServer(0)
    joinServer(1)
    time.sleep(1)
    joinClient(0, 0)
    joinClient(1, 1)

    connectServers(0, 1)

    get(0, "z")
    put(0, "x", 0)
    # get(0, "x")

    put(1, "x", 1)
    put(0, "x", 2)
    put(0, "y", 3)

    print ('-----before stablize')
    debug(get(0, "x"))  # should get 2
    print ('get x from s1: (exp 1)')
    get(1, "x")  # should get 1
    stabilize()
    # time.sleep(1)
    print ('-----after stablize')
    get(1, "x")  # should get 1

