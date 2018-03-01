import argparse
import math

parser = argparse.ArgumentParser()
parser.add_argument("-n", "--groups_num", type = int, default = 2, help = "Number of groyps")
parser.add_argument("file", help = "Name of input file")
args = parser.parse_args()

num = args.groups_num
f = open(args.file)
graph = {}
m = 0
groups = []
pl = []
pairs = []

for line in f:
    a = int(line.split()[0])
    b = int(line.split()[1])
    if a not in graph:
        graph[a] = []
    if b not in graph:
        graph[b] = []
    graph[a].append(b)
    graph[b].append(a)
    pl.append(a)
    pl.append(b)
    pairs.append((a,b))
    m = m + 2
    if [a] not in groups:
        groups.append([a])
    if [b] not in groups:
        groups.append([b])
qprin = 0

while len(groups) > num:
    maxdq = -math.inf
    for pair in pairs:
        a = pair[0]
        b = pair[1]
        for i in groups:
            if a in i:
                xa = groups.index(i)
            if b in i:
                xb = groups.index(i)
        err = 'off'
        if xa == xb:
            pairs.remove(pair)
            err = 'on'
        else:
            test = []
            newteam = groups[xa] + groups[xb]
            for k in groups[:]:
                if k != groups[xa] and k != groups[xb]:
                    test.append(k)
            test.append(newteam)
            qmeta = 0
            for i in range(len(test)):
                ai = 0
                ei = 0
                for j in test[i]:
                    ai = ai + pl.count(j)/m
                    for k in test[i]:
                        if j in graph[k]:
                            ei = ei + 1/m
                qi = ei - ai**2
                qmeta = qmeta + qi
            dq = qmeta - qprin
            if dq > maxdq:
                maxdq = dq
                g = pair
                g1 = xa
                g2 = xb
            del test
    qprin = qprin + maxdq
    if err == 'off':
        pairs.remove(g)
    groups[g1].extend(groups.pop(g2))

sumq = 0
for i in range(len(groups)):
    ai = 0
    ei = 0
    for j in groups[i]:
        ai = ai + pl.count(j)/m
        for k in groups[i]:
            if j in graph[k]:
                ei = ei + 1/m
    qi = ei - ai**2
    sumq = sumq + qi
for j in range(len(groups)):
    groups[j].sort()
groups.sort()
for i in groups:
    print(sorted(i))
print("%.4f" %sumq)
