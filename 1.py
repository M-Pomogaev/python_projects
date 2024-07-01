from scipy.stats import entropy
import numpy as np
import math

q = 3

def pk_sum(k):
    sum = 0
    for i in range(k):
        sum += pk[i]
    return sum

pk = [0.34, 0.18, 0.17, 0.16, 0.15]
pk_ecomulate = [ pk_sum(k) for k in range(5)]
lens = []
print(pk_ecomulate)
for p in pk:
    lens.append(math.ceil(-math.log(p, q)))
print(lens)

for p0, p, l in zip(pk, pk_ecomulate, lens):
    print("p:", p0, "l:", l)
    for i in range(l):
        print(math.floor(int((p := p*q))), end='')
        p = p % 1
    print()

'''
print(entropy(pk))

lens = [1, 2, 2, 2, 2, 2, 2]
sum = 0
for pi, l in zip(pk, lens):
    sum += pi * l

print(sum)
'''