import networkx as nx
import matplotlib.pyplot as plt
import random

BUS_COUNT = 10
BUS_SIZE = 3
ROWDY_GROUPS_MAX = 100
STUDENT_COUNT = BUS_COUNT * BUS_SIZE

G = nx.Graph()

# Complete graph of size 30
for i in range(STUDENT_COUNT):
    G.add_node(i)
for i in range(STUDENT_COUNT):
    for j in range(STUDENT_COUNT):
        if i != j:
            G.add_edge(i, j)


param_file = open('parameters.txt', 'w')
rowdies_graph = nx.Graph()

param_file.write(str(BUS_COUNT) + '\n')
param_file.write(str(BUS_SIZE) + '\n')

#Need to have random rowdy pairs not contradict solution set

# Random rowdy pairs
rowdies = random.sample(range(1, (int) (STUDENT_COUNT * (STUDENT_COUNT - 1) / 2)), ROWDY_GROUPS_MAX)
for i in rowdies:
    u = 1
    counter = 0
    while (counter < i):
        counter += STUDENT_COUNT - u
        u += 1
    v = STUDENT_COUNT - (counter - i)
    param_file.write('[\'' + str(u) + '\', \'' + str(v) + '\'] \n')
    rowdies_graph.add_edge(u, v)


nx.write_gml(G, 'graph.gml', nx.readwrite.gml.literal_stringizer)
nx.draw(rowdies_graph)
plt.savefig('graph.png')
