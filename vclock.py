def from_size(n):
    """
    Constructs a zeroed, *n* sized vector clock.
    """
    return [0] * n


def merge(a, b):
    """
    Given two clocks, return a new clock with all
    values greater or equal to those of the merged
    clocks.
    """
    return list(map(max, zip(a, b)))


def compare(a, b):
    """
    Compares two vector clocks, returns -1 if ``a < b``,
    1 if ``a > b`` else 0 for concurrent events
    or identical values.
    """
    gt = False
    lt = False
    for j, k in zip(a, b):
        gt |= j > k
        lt |= j < k
        if gt and lt:
            break
    return int(gt) - int(lt)


def increment(clock, index):
    """
    Increment the clock at *index*.
    """
    clock[index] += 1
    return


def is_concurrent(a, b):
    """
    Returns whether the given clocks are concurrent.
    They must not be equal in value.
    """

    return (a != b) and compare(a, b) == 0

'''
example code
import vclock  
a = vclock.from_size(3)
b = vclock.from_size(3)
vclock.increment(a, 0)
vclock.increment(b, 1)
c = vclock.merge(a,b)
flag = vclock.is_concurrent(a, c)
print a
print c
print flag

'''