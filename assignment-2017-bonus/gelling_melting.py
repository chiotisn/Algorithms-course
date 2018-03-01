import argparse
import networkx as nx
import numpy as np
import scipy as sp

#arguments
parser = argparse.ArgumentParser()
parser.add_argument("graph", help = "graph file")
parser.add_argument("num_edges", help = "number of edges to delete / add")
parser.add_argument("-g", "--gell", action = "store_true", help = "gell graph")
parser.add_argument("-d", "--directed", action = "store_true", help = "directed graph")
parser.add_argument("-s", "--separator", default = " ", help = "separator")

args = parser.parse_args()
k = int(args.num_edges)
separator = args.separator

#creating graph
f = open(args.graph)
if args.directed:
    g = nx.DiGraph()
else:
    g = nx.Graph()
for line in f:
    a = int(line.split(separator)[0])
    b = int(line.split(separator)[1])
    g.add_edge(a,b)

#computing leading eigenvalue and eigenvectors
adj = nx.adjacency_matrix(g)
l, v = sp.sparse.linalg.eigs(adj.asfptype(), k = 1, which = 'LM', return_eigenvectors=True)
#print(l)
v = np.absolute(v)
if args.directed:
    adjT = adj.copy()
    adjT.transpose()
    t, u = sp.sparse.linalg.eigs(adjT.asfptype(), k = 1, which = 'LM', return_eigenvectors=True)
    u = np.absolute(u)
else:
    u = v.copy() #symmetric matricies have equal left and right eigenvectors
v = np.ravel(v)
u = np.ravel(u)
#print(v)
#print(u)
ans = []

#the answer array
for i in range(k):
    ans.append(((0,0),-1))

if args.gell: #gell algorithm
    if args.directed:
        ind = max(list(g.in_degree().values()))
        outd = max(list(g.out_degree().values()))
    else:
        ind = max(list(g.degree().values()))
        outd = max(list(g.degree().values()))
    sortu = np.ndarray.argsort(u)[::-1]
    sortv = np.ndarray.argsort(v)[::-1]
    #print(sortu, sortv)
    I = []
    J = []
    for r in range(k + ind):
        i = sortu[r]
        I.append((i,g.nodes()[i]))
    for r in range(k + outd):
        i = sortv[r]
        J.append((i,g.nodes()[i]))
    for i in I:
        for j in J:
            if g.has_edge(i[1],j[1]):
                continue
            if args.directed != True and g.has_edge(j[1],i[1]):
                continue
            if i == j:
                continue
            score = u.item(i[0])*v.item(j[0])
            if args.directed == True:
                if min(ans, key = lambda x: x[1])[1] < score:
                    ans[ans.index(min(ans, key = lambda x: x[1]))] = ((i[1],j[1]), score)
            else:
                if min(ans, key = lambda x: x[1])[1] < score and (j[1],i[1]) not in [i[0] for i in ans]:
                    ans[ans.index(min(ans, key = lambda x: x[1]))] = ((i[1],j[1]), score)
    ans.sort(reverse = True, key=lambda x: x[1])
    for i in ans:
        print(i)
else: #melt algorithm
    for e in g.edges():
        i = g.nodes().index(e[0])
        j = g.nodes().index(e[1])
        score = u.item(i)*v.item(j)
        if min(ans, key = lambda x: x[1])[1] < score:
            ans[ans.index(min(ans, key = lambda x: x[1]))] = (e, score)
    ans.sort(reverse = True, key=lambda x: x[1])
    for i in ans:
        print(i)
