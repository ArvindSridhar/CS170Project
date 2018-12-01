# varname = 'z_' + str(i) + '_' + str(node2hash[edge[0]]) + '_' + str(node2hash[edge[1]])
		# keyname = 'z' + str(i) + '[' + str(node2hash[edge[0]]) + '][' + str(node2hash[edge[1]]) + ']'
		# x = pulp.LpVariable(varname, cat='Integer')
		# variables[keyname] = x
		# need to update

# LpAffineExpression([ (x[0],1), (x[1],-3), (x[2],4)])

# Initialize c(u, v) for all u, v
# c = np.zeros((n, n))
# for edge in edges:
# 	u = node2hash[edge[0]]
# 	v = node2hash[edge[1]]
# 	c[u][v] = 1


# my_lp_problem = pulp.LpProblem("My LP Problem", pulp.LpMaximize)

# x = pulp.LpVariable('x', lowBound=0, cat='Continuous')
# y = pulp.LpVariable('y', lowBound=2, cat='Continuous')

# # Objective function
# my_lp_problem += 4 * x + 3 * y, "Z"

# # Constraints
# my_lp_problem += 2 * y <= 25 - x
# my_lp_problem += 4 * y >= 2 * x - 8
# my_lp_problem += y <= 2 * x - 5