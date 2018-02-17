import unittest
import sys
from master import *

debugV = 0
def debug(s):
    global  debugV

    print(str(s)  + " debug information " + str(debugV))
    debugV = debugV +1


# TESTING
debug("ffff")

debug("fffwwwww")
joinServer(0)
joinServer(1)
time.sleep(1)
joinClient(0, 0)
joinClient(1, 1)

connectServers(0,1)

get(0, "z")
put(0, "x", 0)
#get(0, "x")

put(1, "x", 1)
put(0,"x", 2)
put(0,"y", 3)

print ('-----before stablize')
debug(get(0, "x")) # should get 2
print ('get x from s1: (exp 1)')
get(1, "x") # should get 1
stabilize()
#time.sleep(1)
print ('-----after stablize')
get(1, "x") # should get 1