import argparse
import sys
import random

parser = argparse.ArgumentParser()
parser.add_argument("elements", type = int, help = "Number of elements")
args = parser.parse_args()
n = args.elements

d = []
lend = n*(n-1)/6
pairs = []
covered = []
ap = {}

for i in range(n+1):
    ap[i] = 0

if not(n%6 == 1 or n%6 == 3) and n >= 3:
    sys.exit("ERROR: The number of elements must be of the form 6*k+1 or 6*k+3 for some k and greater than or equal to 3")

for i in range(1,n+1):
    for j in range(1,n+1):
        if i == j:
            continue
        pairs.append([i,j])

while lend > 0:
    while True:
        i = random.randint(1,n)
        if ap[i] < (n-1)/2:
            x = i
            break
    p1 = [0,0]
    while sorted(p1) in covered or p1[0] != x:
        p1 = random.choice(pairs)
    p2 = [0,0]
    while sorted(p2) in covered or p2[0] != x or p1 == p2:
        p2 = random.choice(pairs)
    if sorted([p1[1], p2[1]]) in covered:
        for i in d:
            if p1[1] in i and p2[1] in i:
                covered.remove(sorted([i[0],i[1]]))
                covered.remove(sorted([i[0],i[2]]))
                covered.remove(sorted([i[1],i[2]]))
                ap[i[0]] -= 1
                ap[i[1]] -= 1
                ap[i[2]] -= 1
                d.remove(i)
                lend += 1
                break
    covered.append(sorted(p1))
    covered.append(sorted(p2))
    covered.append(sorted([p1[1],p2[1]]))
    ap[p1[0]] += 1
    ap[p1[1]] += 1
    ap[p2[1]] += 1
    block = [p1[0], p1[1], p2[1]]
    block.sort()
    d.append(tuple(block))
    lend -= 1
print(sorted(d))
print(len(d))
