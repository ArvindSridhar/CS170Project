import networkx as nx
import os

###########################################
# Change this variable to the path to
# the folder containing all three input
# size category folders
###########################################
path_to_inputs = "./all_inputs"

###########################################
# Change this variable if you want
# your outputs to be put in a
# different folder
###########################################
path_to_outputs = "./all_outputs_greedy"

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
