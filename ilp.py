import gurobipy as gp
from gurobipy import GRB
from math import lcm

# Function to read input from a file
def read_input(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    # Extract number of tasks and processors
    n, m = map(int, lines[0].strip().split())

    # Extract task parameters (e_i, p_i, m_i, k_i)
    tasks = []
    for line in lines[1:]:
        tasks.append(tuple(map(int, line.strip().split())))

    return n, m, tasks

# Read input from the text file
n, m, tasks = read_input('input_parameters.txt')

# Hyper period
periods = [task[1] for task in tasks]
h_p = lcm(*periods)  # calculating the hyper period

# Number of jobs in hyper period for each task
ni = [h_p // task[1] for task in tasks]

# Creating the model
model = gp.Model("MNP-WHRT")

# Decision variables
X = model.addVars(range(1, n + 1), range(1, m + 1), vtype=GRB.BINARY, name="X")
Y = model.addVars(range(1, n + 1), range(1, max(ni) + 1), vtype=GRB.BINARY, name="Y")
Z = model.addVars(range(1, m + 1), vtype=GRB.BINARY, name="Z")

# Objective function to minimize the number of processors
model.setObjective(gp.quicksum(Z[l] for l in range(1, m + 1)), GRB.MINIMIZE)

# Constraints

M = n + 1

# C1 - Task is always mapped to one processor
for i in range(1, n + 1):
    model.addConstr(gp.quicksum(X[i, l] for l in range(1, m + 1)) == 1, name="C1_task")

# C2 - (m, k) constraint should be satisfied for k_i jobs
for i, task in enumerate(tasks, start=1):
    ei, pi, mi, ki = task
    n_i = ni[i - 1]

    # Calculate the number of windows w of size k_i
    w = n_i - ki + 1

    # Loop over all windows
    for z in range(1, w + 1):  # z starts from 1
        model.addConstr(gp.quicksum(Y[i, j] for j in range(z, z + ki)) >= mi, name="C2_task")

# C3 - All accepted jobs mapped to a processor must be feasible to be scheduled by EDF
time_points = sorted({(j - 1) * task[1] for i, task in enumerate(tasks, start=1) for j in range(1, ni[i - 1] + 1)} |
                     {j * task[1] for i, task in enumerate(tasks, start=1) for j in range(1, ni[i - 1] + 1)})

for l in range(1, m + 1):
    for t1 in time_points:
        for t2 in time_points:
            if t2 > t1:
                model.addConstr(
                    gp.quicksum(X[i, l] * Y[i, j] * tasks[i - 1][0] for i in range(1, n + 1) for j in range(1, ni[i - 1] + 1)
                                if (j - 1) * tasks[i - 1][1] >= t1 and j * tasks[i - 1][1] <= t2) <= t2 - t1,
                    name="C3_constraint"
                )

# Additional constraints

for l in range(1, m + 1):
    model.addConstr(gp.quicksum(X[i, l] for i in range(1, n + 1)) <= M * Z[l], name="C4")
    model.addConstr(Z[l] <= gp.quicksum(X[i, l] for i in range(1, n + 1)), name="C5")

# Optimization of the model
model.optimize()

# Output the results
if model.status == GRB.OPTIMAL:
    print(f"\n Optimal number of processors: {model.objVal}")

    for i in range(1, n + 1):
        for l in range(1, m + 1):
            if X[i, l].x == 1:
                print(f"\n Task {i} is assigned to Processor {l}\n")
    for i in range(1, n + 1):
        for j in range(1, ni[i - 1] + 1):
            if Y[i, j].x == 1:
                print(f"Job {j} of Task {i} is accepted")
else:
    print("No optimal solution found")