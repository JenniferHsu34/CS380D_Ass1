import unittest
import sys
import master
print 'here?#################################'
'''

class TestKV(unittest.TestCase):



    def test_1(self): # test get with invalid key
        joinServer(0)
        joinServer(1)

        joinClient(0, 0)
        joinClient(1, 1)
        self.assertEqual(get(0, "x"), 'ERR_KEY', 'invalid key')
    def test_2(self): # test get with valid key
        put(0, "x", 0)
        put(1, "x", 1)

        self.assertEqual(get(0, "x"), 0)
        self.assertEqual(get(1, "x"), 1)

    def test_3(self): # put more value and check wlog
        put(0, "x", 3)
        put(0, "y", 3)
        curLog0 =  [sys.maxsize, 1, 0, ('x', 0)], \
                         [sys.maxsize, 2, 0, ('x', 3)], [sys.maxsize, 3, 0, ('y', 3)]
        self.assertEqual(curLog0, servers[0].writeLog)
        curLog1 =  [sys.maxsize, 1, 1, ('x', 1)]
        self.assertEqual(curLog1, servers[1].writeLog)

    def test_4(self): # stablize
        stabilize()
        

if __name__ == '__main__':
    unittest.main()
#
'''
print 'here?#################################'
joinServer(0)
print 'here?#################################'
joinServer(1)
print 'here?#################################'

joinClient(0, 0)
print 'here?#################################'
joinClient(1, 1)
print 'here?################'
connectServers(0,1)
print 'here?#'
print get(0, "z")
put(0, "x", 0)
put(1, "x", 1)
put(0,"x", 2)
put(0,"y", 3)
print '-----before stablize'
print '[s0]', servers[0].vclock, servers[0].writeLog
print '[s1]', servers[1].vclock, servers[1].writeLog
print 'get x from s0: (exp 2) ', get(0, "x") # should get 2
print 'get x from s1: (exp 1)', get(1, "x") # should get 1
stabilize()
print '-----after stablize'
print '[s0]', servers[0].vclock, servers[0].writeLog #vclock -> 3, 1, 0, 0
print '[s1]', servers[1].vclock, servers[1].writeLog #vclock -> 3, 1, 0, 0
print 'get x from s1: (exp 2 since it did anti entropy)', get(1, "x") # should get 1
#joinClient(1,0)

