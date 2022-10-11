#!/usr/bin/python

from random import random

L = 22 + 5
k = list(range(L))
for i in range(L):
    j = i + int((L-i)*random())
    k[i], k[j] = k[j], k[i]
A = 0x5D0
d = { chr(i+A) : chr(v+A) for i,v in enumerate(k) }
print(d)

fname = 'text.txt'
f = open(fname, 'r')
t = f.read()
f.close()

fname = 'out.txt'
f=open(fname, 'w')
for a in t:
    f.write(d.get(a,a))
f.close()

