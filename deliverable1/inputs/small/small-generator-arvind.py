import networkx as nx
import matplotlib.pyplot as plt
import random

# Setting constants
BUS_COUNT = 5
BUS_SIZE = 10
EXTRA_FRIEND_CONNS = 15
NUM_ROWDY_GROUPS = 100
ROWDY_GROUP_MAX_SIZE = 10
NUM_STUDENTS = BUS_COUNT * BUS_SIZE
INPUT_SIZE = 'small'

# Initializing graph parameters
G = nx.Graph()
V = {}

# Constructing the friend graph
count = 0
for i in range(BUS_COUNT):
	for j in range(BUS_SIZE):
		G.add_node(count + j)
		V[count + j] = i
		# print("Added node", count + j)
	for j in range(BUS_SIZE):
		for k in range(BUS_SIZE):
			if count + j != count + k:
				G.add_edge(count + j, count + k)
				# print("Added edge", count + j, "to", count + k)
	count += BUS_SIZE
for i in range(EXTRA_FRIEND_CONNS):
	j = random.randint(0, NUM_STUDENTS-1)
	k = random.choice(list(range(0, j)) + list(range(j+1, NUM_STUDENTS)))
	G.add_edge(j, k)
	# print("Added edge", j, "to", k)
print("Finished Constructing Graph")

# Writing the graph to file
nx.write_gml(G, 'graph.gml', nx.readwrite.gml.literal_stringizer)
nx.draw(G)
plt.savefig('graph.png')
print("Finished Printing Graph")

# Starting the parameter file
param_file = open('parameters.txt', 'w')
param_file.write(str(BUS_COUNT) + '\n')
param_file.write(str(BUS_SIZE) + '\n')

# Rowdy group generation
rowdy_groups = []
count = 0
while count < NUM_ROWDY_GROUPS:
	num_in_group = random.randint(ROWDY_GROUP_MAX_SIZE - 2, ROWDY_GROUP_MAX_SIZE) # Can tune this range
	group = []
	for i in range(num_in_group):
		j = random.choice([elem for elem in range(NUM_STUDENTS) if elem not in group])
		group.append(j)
	if len(set([V[elem] for elem in group])) != 1:
		rowdy_groups.append(group)
		count += 1
for group in rowdy_groups:
	group = [str(elem) for elem in group]
	param_file.write(str(group) + '\n')
print("Finished Generating Rowdy Groups")

output_file = open('../../outputs/' + INPUT_SIZE + '.out', 'w')
assignments = {}
for node, bus_num in V.items():
	assignments.setdefault(bus_num, []).append(node)
assignments = list(assignments.values())
for group in assignments:
	group = [str(elem) for elem in group]
	output_file.write(str(group) + '\n')
print("Finished Creating Output File")
