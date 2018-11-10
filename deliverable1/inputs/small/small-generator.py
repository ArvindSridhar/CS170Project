import networkx as nx
import matplotlib.pyplot as plt
import random

INPUT_SIZE = 'small'
BUS_COUNT = 3
BUS_SIZE = 10
ROWDY_GROUPS_MAX = 100
MIN_ROWDY_GROUP_SIZE = 5
STUDENT_COUNT = BUS_COUNT * BUS_SIZE
EXTRA_CONNECTIONS = STUDENT_COUNT

G = nx.Graph()

# Graph of size STUDENT_COUNT
students = [i for i in range(STUDENT_COUNT)]
for student in students:
    G.add_node(student)

# Create groups of size BUS_SIZE
random.shuffle(students)
buses = [];
for bus_num in range(BUS_COUNT):
    first = BUS_SIZE * bus_num;
    buses.append([students[first + i] for i in range(BUS_SIZE)])

# Fully connect these groups
for bus in buses:
    for first_student_index in range(BUS_SIZE):
        for second_student_index in range(first_student_index + 1, BUS_SIZE):
            G.add_edge(bus[first_student_index], bus[second_student_index])

# Place these groups in output
output_file = open('../../outputs/' + INPUT_SIZE + '/' + INPUT_SIZE + '.out', 'w')
for bus in buses:
    output_file.write(str([str(i) for i in bus]) + '\n')

# Draw solution in solution.png
# nx.draw(G)
# plt.savefig('solution.png')

# Add EXTRA_CONNECTIONS number of extra connections
for i in range(EXTRA_CONNECTIONS):
    random_buses = random.sample(range(BUS_COUNT), 2)
    random_indices = random.sample(range(BUS_SIZE), 2)
    student_1 = buses[random_buses[0]][random_indices[0]]
    student_2 = buses[random_buses[1]][random_indices[1]]
    G.add_edge(student_1, student_2)

# Draw graph of student connections in connections.png
# nx.draw(G)
# plt.savefig('connections.png')

# Write graph of student connections to graph.gml
nx.write_gml(G, 'graph.gml', nx.readwrite.gml.literal_stringizer)


param_file = open('parameters.txt', 'w')
rowdies_graph = nx.Graph()

param_file.write(str(BUS_COUNT) + '\n')
param_file.write(str(BUS_SIZE) + '\n')

# Rowdy group generation
rowdy_groups = []
for group in range(ROWDY_GROUPS_MAX):
    group_size = random.choice(range(MIN_ROWDY_GROUP_SIZE, BUS_SIZE))
    random_buses = random.sample(range(BUS_COUNT), 2)
    random_indices = random.sample(range(BUS_SIZE), 2)
    student_1 = buses[random_buses[0]][random_indices[0]]
    student_2 = buses[random_buses[1]][random_indices[1]]
    remaining = [elem for elem in range(STUDENT_COUNT) if elem != student_1 and elem != student_2]
    sample_remaining = random.sample(remaining, group_size - 2)
    rowdy_groups.append([student_1] + [student_2] + sample_remaining)

# Write rowdy groups to parameters.txt
for group in rowdy_groups:
    param_file.write(str([str(i) for i in group]) + '\n')

# Draw rowdy groups in graph.png
# nx.draw(rowdies_graph)
# plt.savefig('graph.png')
