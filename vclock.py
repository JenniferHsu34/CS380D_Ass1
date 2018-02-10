class vclock:

    def __init__(self, n, sid):
        """
        Constructs a zeroed, *n* sized vector clock.
        """
        self.vclock = [0] * n
        self.sid = sid


    def merge(self, b):
        """
        Given two clocks, return a new clock with all
        values greater or equal to those of the merged
        clocks.
        """
        self.vclock = list(map(max, zip(self.vclock, b)))

    def getTimestamp(self):
        return self.vclock[self.sid]

    def compare(self, b):
        """
        Compares two vector clocks, returns -1 if ``a < b``,
        1 if ``a > b`` else 0 for concurrent events
        or identical values.
        """
        gt = False
        lt = False
        for j, k in zip(self.vclock, b):
            gt |= j > k
            lt |= j < k
            if gt and lt:
                break
        return int(gt) - int(lt)


    def increment(self):
        """
        Increment the clock at *index*.
        """
        self.vclock[self.sid] = max(self.vclock) + 1
        return


    def isConcurrent(self, b):
        """
        Returns whether the given clocks are concurrent.
        They must not be equal in value.
        """

        return (self.vclock != b) and self.compare(self.vclock, b) == 0

'''
example code
import vclock  
a = vclock(3)
b = vclock(3)
a.increment()    
b.increment()
a.merge(b.vclock)
flag = vclock.is_concurrent(a, c)
print a
print c
print flag
'''

a = vclock(3, 0)
b = vclock(3, 1)
c = vclock(3, 2)
a.increment()
a.increment()
print(a.vclock)
b.merge(a.vclock)
print(b.vclock)
b.increment()
print(b.vclock)
