import networkx as nx
import os

###########################################
# Change this variable to the path to
# the folder containing all three input
# size category folders
###########################################
path_to_inputs = "./all_large_inputs"

###########################################
# Change this variable if you want
# your outputs to be put in a
# different folder
###########################################
path_to_outputs = "./all_large_outputs"

def parse_input(folder_name):
    '''
        Parses an input and returns the corresponding graph and parameters

        Inputs:
            folder_name - a string representing the path to the input folder

        Outputs:
            (graph, num_buses, size_bus, constraints)
            graph - the graph as a NetworkX object
            num_buses - an integer representing the number of buses you can allocate to
            size_buses - an integer representing the number of students that can fit on a bus
            constraints - a list where each element is a list vertices which represents a single rowdy group
    '''
    graph = nx.read_gml(folder_name + "/graph.gml")
    parameters = open(folder_name + "/parameters.txt")
    num_buses = int(parameters.readline())
    size_bus = int(parameters.readline())
    constraints = []
    for line in parameters:
        line = line[1: -2]
        curr_constraint = [num.replace("'", "") for num in line.split(", ")]
        constraints.append(curr_constraint)
    return graph, num_buses, size_bus, constraints

def solve(graph, num_buses, size_bus, constraints):
    #TODO: Write this method as you like. We'd recommend changing the arguments here as well
    solution = ""
    sol_array = greedy_solve(graph, num_buses, size_bus, constraints)
    for bus in sol_array:
        solution += '[' + str(bus)[1:-1] + ']' + '\n'
    return solution

def greedy_solve(graph, num_buses, size_bus, constraints):
    students = list(graph.nodes())
    buses = [[] for _ in range(num_buses)]
    for student in students:
        empty_improve = 1
        if empty_buses(buses) == remaining_students(students, student):
            empty_improve = 1000000
        connections = [num_connections(bus, graph, student) for bus in buses]
        can_add_bus = [can_add(bus, student, size_bus) for bus in buses]
        negated = 0
        for i in range(len(buses)):
            if not can_add(buses[i], student, size_bus):
                connections[i] = -1
                negated += 1
            if len(buses[i]) == 0:
                connections[i] += empty_improve
        for i in range(num_buses - negated):
            if i == num_buses - negated - 1:
                max_connection_bus = connections.index(max(connections))
                buses[max_connection_bus].append(student)
                break
            max_connection_bus = connections.index(max(connections))
            if not is_rowdy(buses[max_connection_bus], student, constraints):
                buses[max_connection_bus].append(student)
                break
            connections[max_connection_bus] = -1
    return buses

# Returns the number of connections a student has in a given bus
def num_connections(bus, graph, student):
    ans = 0
    for friend in list(graph.adj[student]):
        if friend in bus:
            ans += 1
    return ans

# Checks for bus size constraint
def can_add(bus, student, size_bus):
    return len(bus) < size_bus

# Checks for rowdiness
def is_rowdy(bus, student, constraints):
    bus = bus + [student]
    for constraint in constraints:
        if all(kid in bus for kid in constraint):
            return True
    return False

# Counts empty buses
def empty_buses(buses):
    ans = 0
    for bus in buses:
        if not bus:
            ans += 1
    return ans

# Count remaining students
def remaining_students(students, student):
    return len(students) - students.index(student)

def main():
    '''
        Main method which iterates over all inputs and calls `solve` on each.
        The student should modify `solve` to return their solution and modify
        the portion which writes it to a file to make sure their output is
        formatted correctly.
    '''
    size_categories = ["large"]
    if not os.path.isdir(path_to_outputs):
        os.mkdir(path_to_outputs)

    for size in size_categories:
        category_path = path_to_inputs + "/" + size
        output_category_path = path_to_outputs + "/" + size
        category_dir = os.fsencode(category_path)

        if not os.path.isdir(output_category_path):
            os.mkdir(output_category_path)

        for input_folder in os.listdir(category_dir):
            input_name = os.fsdecode(input_folder)
            if input_name == '198' or input_name == '.DS_Store':
                continue
            graph, num_buses, size_bus, constraints = parse_input(category_path + "/" + input_name)
            solution = solve(graph, num_buses, size_bus, constraints)
            output_file = open(output_category_path + "/" + input_name + ".out", "w")

            #TODO: modify this to write your solution to your
            #      file properly as it might not be correct to
            #      just write the variable solution to a file
            output_file.write(solution)

            output_file.close()

if __name__ == '__main__':
    main()

# -------------------------------------------------------------------
# Our alternate ILP solution
# -------------------------------------------------------------------
# import networkx as nx
# import matplotlib.pyplot as plt
# import random
# import pulp
# import numpy as np
# import time

# for input_example in range(1, 332):
#     # Read in the graph
#     path_to_graph = 'all_inputs/large/' + str(input_example) + '/graph.gml'
#     try:
#         G = nx.read_gml(path=path_to_graph)
#     except:
#         continue
#     nodes = list(G.nodes())
#     n = len(nodes)
#     edges = list(G.edges())

#     # Remove duplicate edges
#     edge_set = set({})
#     for edge in edges:
#         edge_set.add(tuple(sorted(edge)))
#     edges = list(edge_set)

#     # Hash nodes
#     node2hash, hash2node, count = {}, {}, 0
#     for node in nodes:
#         node2hash[node] = count
#         hash2node[count] = node
#         count += 1

#     # Get parameters for problem
#     path_to_params = 'all_inputs/large/' + str(input_example) + '/parameters.txt'
#     with open(path_to_params) as f:
#         params = (f.read()).split('\n')
#         params = [e for e in params if e != ""]
#     BUS_COUNT = int(params[0]) # k
#     BUS_SIZE = int(params[1]) # s
#     rowdies = [eval(e) for e in params[2:]]

#     # Define the linear programming problem
#     lp_problem = pulp.LpProblem("Optimizing_Bus_Assignments", pulp.LpMinimize)

#     # Initialize the variables bi(u)
#     variables = {}
#     for i in range(BUS_COUNT):
#         for u in range(n):
#             varname = 'b' + str(i) + '_' + str(u)
#             keyname = 'b[' + str(i) + '][' + str(u) + ']'
#             x = pulp.LpVariable(varname, lowBound=0, upBound=1, cat='Integer')
#             variables[keyname] = x

#     # Initialize the variables zi(u, v)+ and zi(u, v)-
#     for i in range(BUS_COUNT):
#         for edge in edges:
#             u = str(node2hash[edge[0]])
#             v = str(node2hash[edge[1]])
#             varname1 = 'z_' + str(i) + '_' + u + '_' + v + '_' + 'plus'
#             keyname1 = 'z' + str(i) + '[' + u + '][' + v + ']+'
#             varname2 = 'z_' + str(i) + '_' + u + '_' + v + '_' + 'minus'
#             keyname2 = 'z' + str(i) + '[' + u + '][' + v + ']-'
#             x = pulp.LpVariable(varname1, cat='Continuous')
#             y = pulp.LpVariable(varname2, cat='Continuous')
#             variables[keyname1] = x
#             variables[keyname2] = y

#     # Define the objective function
#     func = ''
#     for i in range(BUS_COUNT):
#         for edge in edges:
#             u = str(node2hash[edge[0]])
#             v = str(node2hash[edge[1]])
#             func += variables['z' + str(i) + '[' + u + '][' + v + ']+']
#             func += variables['z' + str(i) + '[' + u + '][' + v + ']-']
#     lp_problem += func, "Z"

#     # Constraint 1: zi(u, v)+ - zi(u, v)- = bi(v) - bi(u), zi(u, v)+ ≥ 0, zi(u, v)- ≥ 0
#     for i in range(BUS_COUNT):
#         for edge in edges:
#             u = str(node2hash[edge[0]])
#             v = str(node2hash[edge[1]])
#             lp_problem += variables['z' + str(i) + '[' + u + '][' + v + ']+'] - variables['z' + str(i) + '[' + u + '][' + v + ']-'] >= variables['b[' + str(i) + '][' + v + ']'] - variables['b[' + str(i) + '][' + u + ']']
#             lp_problem += variables['z' + str(i) + '[' + u + '][' + v + ']+'] - variables['z' + str(i) + '[' + u + '][' + v + ']-'] <= variables['b[' + str(i) + '][' + v + ']'] - variables['b[' + str(i) + '][' + u + ']']
#             lp_problem += variables['z' + str(i) + '[' + u + '][' + v + ']+'] >= 0
#             lp_problem += variables['z' + str(i) + '[' + u + '][' + v + ']-'] >= 0

#     # Constraint 2: ∑bi(u) over all i = 1, for all u in V
#     for u in range(n):
#         func = ''
#         for i in range(BUS_COUNT):
#             func += variables['b[' + str(i) + '][' + str(u) + ']']
#         lp_problem += func <= 1
#         lp_problem += func >= 1

#     # Constraint 3: ∑bi(u) over all u ≤ BUS_SIZE, for all i
#     for i in range(BUS_COUNT):
#         func = ''
#         for u in range(n):
#             func += variables['b[' + str(i) + '][' + str(u) + ']']
#         lp_problem += func <= BUS_SIZE#BUS_SIZE//2
#         lp_problem += func >= 1

#     # Constraint 4: rowdies
#     for i in range(BUS_COUNT):
#         for j in range(len(rowdies)):
#             Lj = rowdies[j]
#             func = ''
#             for k in range(len(Lj)):
#                 u = str(node2hash[Lj[k]])
#                 func += variables['b[' + str(i) + '][' + u + ']']
#             lp_problem += func <= len(Lj) - 1

#     # Solve the linear program
#     print('starting to solve')
#     start = time.time()
#     lp_problem.solve() #pulp.solvers.GLPK_CMD(), pulp.solvers.COINMP_DLL(timeLimit=30))
#     end = time.time()
#     print(end - start, 'seconds taken')

#     # Get the variables
#     solved_vars = lp_problem.variables()
#     solved_bs = solved_vars[:n*BUS_COUNT]
#     final_values = {b.name: b.varValue for b in solved_bs}
#     student_assignments = [-50]*n
#     for u in range(n):
#         max_bus, maximizer = -50, 0
#         for i in range(BUS_COUNT):
#             score = final_values['b' + str(i) + '_' + str(u)]
#             if score >= maximizer:
#                 max_bus, maximizer = i, score
#         student_assignments[u] = max_bus
#     final_assignments = {}
#     for i in range(BUS_COUNT):
#         final_assignments[i] = [idx for idx in range(len(student_assignments)) if student_assignments[idx] == i]

#     # Write to output file
#     output_file = open('all_outputs/large/' + str(input_example) + '.out', 'w')
#     for bus in final_assignments:
#         output_file.write("['" + "', '".join([hash2node[u] for u in final_assignments[bus]]) + "']\n")
