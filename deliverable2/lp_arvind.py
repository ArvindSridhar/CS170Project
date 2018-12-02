import networkx as nx
import matplotlib.pyplot as plt
import random
import pulp
import numpy as np
import time

for input_example in range(1, 332): #21, 22
	# Read in the graph
	path_to_graph = 'all_inputs/small/' + str(input_example) + '/graph.gml'  #lcarge//1000 #scmall//146
	try:
		G = nx.read_gml(path=path_to_graph)
	except:
		continue
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
	path_to_params = 'all_inputs/small/' + str(input_example) + '/parameters.txt'
	with open(path_to_params) as f:
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
		lp_problem += func <= BUS_SIZE#BUS_SIZE//2
		lp_problem += func >= 1

	# Constraint 4: rowdies
	for i in range(BUS_COUNT):
		for j in range(len(rowdies)):
			Lj = rowdies[j]
			func = ''
			for k in range(len(Lj)):
				u = str(node2hash[Lj[k]])
				func += variables['b[' + str(i) + '][' + u + ']']
			lp_problem += func <= len(Lj) - 1

	# Solve the linear program
	print('starting to solve')
	start = time.time()
	lp_problem.solve(pulp.solvers.GLPK_CMD()) # TODO CHANGE SOLVER HERE: something like lp_problem.solve(pulp.solvers.COINMP_DLL(timeLimit=30))
	end = time.time()
	print(end - start, 'seconds taken')

	# Get the variables
	solved_vars = lp_problem.variables()
	solved_bs = solved_vars[:n*BUS_COUNT]
	final_values = {b.name: b.varValue for b in solved_bs}
	student_assignments = [-50]*n
	for u in range(n):
		max_bus, maximizer = -50, 0
		for i in range(BUS_COUNT):
			score = final_values['b' + str(i) + '_' + str(u)]
			if score > maximizer:
				max_bus, maximizer = i, score
		student_assignments[u] = max_bus
	final_assignments = {}
	for i in range(BUS_COUNT):
		final_assignments[i] = [idx for idx in range(len(student_assignments)) if student_assignments[idx] == i]

	# Write to output file
	output_file = open('all_outputs/small/' + str(input_example) + '.out', 'w')
	for bus in final_assignments:
		output_file.write("['" + "', '".join([hash2node[u] for u in final_assignments[bus]]) + "']\n")
