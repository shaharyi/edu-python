#!/usr/bin/python

import sys

#fname = 'text.txt'
#f = open(fname, 'r')
#t = f.read()
t = sys.stdin.read()
#f.close()

A = 0x5D0
L = 22+5

f = {}
for a in t:
    r = ord(a)
    if r>=A and r<=A+L:
        f[r] = f.get(r,0) + 1
print(f)
p = { chr(a): f[a]  for a in f.keys() } 
print(p)   
p = sorted(p, key=p.get)
print(p)
