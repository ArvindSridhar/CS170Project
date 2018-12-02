import networkx as nx
import matplotlib.pyplot as plt
import random
import pulp
import numpy as np
import time

# Read in the graph
G = nx.read_gml(path='all_inputs/small/145/graph.gml') #large//1000 #small//146
nodes = list(G.nodes())
n = len(nodes)
edges = list(G.edges())

# Remove duplicate edges
edge_set = set({})
for edge in edges:
	edge_set.add(tuple(sorted(edge)))
edges = list(edge_set)

# Hash nodes
node2hash, hash2node, count = {}, {}, 0
for node in nodes:
	node2hash[node] = count
	hash2node[count] = node
	count += 1

# Get parameters for problem
with open('all_inputs/small/145/parameters.txt') as f:
	params = (f.read()).split('\n')
	params = [e for e in params if e != ""]
BUS_COUNT = int(params[0]) # k
BUS_SIZE = int(params[1]) # s
rowdies = [eval(e) for e in params[2:]]

# Define the linear programming problem
lp_problem = pulp.LpProblem("Optimizing_Bus_Assignments", pulp.LpMinimize)

# Initialize the variables bi(u)
variables = {}
for i in range(BUS_COUNT):
	for u in range(n):
		varname = 'b' + str(i) + '_' + str(u)
		keyname = 'b[' + str(i) + '][' + str(u) + ']'
		x = pulp.LpVariable(varname, lowBound=0, upBound=1, cat='Integer') #lowBound=0, upBound=1, cat='Integer'
		variables[keyname] = x

# Initialize the variables zi(u, v)+ and zi(u, v)-
for i in range(BUS_COUNT):
	for edge in edges:
		u = str(node2hash[edge[0]])
		v = str(node2hash[edge[1]])
		varname1 = 'z_' + str(i) + '_' + u + '_' + v + '_' + 'plus'
		keyname1 = 'z' + str(i) + '[' + u + '][' + v + ']+'
		varname2 = 'z_' + str(i) + '_' + u + '_' + v + '_' + 'minus'
		keyname2 = 'z' + str(i) + '[' + u + '][' + v + ']-'
		x = pulp.LpVariable(varname1, cat='Continuous')
		y = pulp.LpVariable(varname2, cat='Continuous')
		variables[keyname1] = x
		variables[keyname2] = y

# Define the objective function
func = ''
for i in range(BUS_COUNT):
	for edge in edges:
		u = str(node2hash[edge[0]])
		v = str(node2hash[edge[1]])
		func += variables['z' + str(i) + '[' + u + '][' + v + ']+']
		func += variables['z' + str(i) + '[' + u + '][' + v + ']-']
lp_problem += func, "Z"

# Constraint 1: zi(u, v)+ - zi(u, v)- = bi(v) - bi(u), zi(u, v)+ ≥ 0, zi(u, v)- ≥ 0
for i in range(BUS_COUNT):
	for edge in edges:
		u = str(node2hash[edge[0]])
		v = str(node2hash[edge[1]])
		lp_problem += variables['z' + str(i) + '[' + u + '][' + v + ']+'] - variables['z' + str(i) + '[' + u + '][' + v + ']-'] >= variables['b[' + str(i) + '][' + v + ']'] - variables['b[' + str(i) + '][' + u + ']']
		lp_problem += variables['z' + str(i) + '[' + u + '][' + v + ']+'] - variables['z' + str(i) + '[' + u + '][' + v + ']-'] <= variables['b[' + str(i) + '][' + v + ']'] - variables['b[' + str(i) + '][' + u + ']']
		lp_problem += variables['z' + str(i) + '[' + u + '][' + v + ']+'] >= 0
		lp_problem += variables['z' + str(i) + '[' + u + '][' + v + ']-'] >= 0

# Constraint 2: ∑bi(u) over all i = 1, for all u in V
for u in range(n):
	func = ''
	for i in range(BUS_COUNT):
		func += variables['b[' + str(i) + '][' + str(u) + ']']
	lp_problem += func <= 1
	lp_problem += func >= 1

# Constraint 3: ∑bi(u) over all u ≤ BUS_SIZE, for all i
for i in range(BUS_COUNT):
	func = ''
	for u in range(n):
		func += variables['b[' + str(i) + '][' + str(u) + ']']
	lp_problem += func <= BUS_SIZE
	lp_problem += func >= 1

# Constraint 4: rowdies
# TODO: need to implement

# Solve the linear program
print('starting to solve')
start = time.time()
lp_problem.solve() # TODO CHANGE SOLVER HERE: something like lp_problem.solve(pulp.solvers.COINMP_DLL(timeLimit=30))
end = time.time()
print(end - start, 'seconds taken')
# lp_problem.writeLP('finalLP.txt')

# Get the variables
solved_vars = lp_problem.variables()
solved_bs = solved_vars[:n*BUS_COUNT]
final_values = {b.name: b.varValue for b in solved_bs}
print(final_values)
student_assignments = [-50]*n
for i in range(BUS_COUNT):
	for u in range(n):
		if final_values['b' + str(i) + '_' + str(u)] > 0.5: # can change
			student_assignments[u] = i
print(student_assignments)
