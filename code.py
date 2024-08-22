import gurobipy as gp
from gurobipy import GRB
from math import lcm

# Example input parameters
n = 2  # Number of tasks
m = 2  # Number of processors
tasks = [(2, 4, 1, 2), (5, 6, 1, 2)]  # (ei, pi, mi, ki) for each task

# Compute hyper-period h
periods = [task[1] for task in tasks]
h = lcm(*periods)

# Compute number of jobs ni for each task in the hyper-period h
ni = [h // task[1] for task in tasks]

# Create a new model
model = gp.Model("MNP-Weakly")

# Decision variables
X = model.addVars(range(1, n + 1), range(1, m + 1), vtype=GRB.BINARY, name="X")  # X[i,l] -> task Ti on processor Pl
Y = model.addVars(range(1, n + 1), range(1, max(ni) + 1), vtype=GRB.BINARY, name="Y")  # Y[i,j] -> job Ti,j is accepted
Z = model.addVars(range(1, m + 1), vtype=GRB.BINARY, name="Z")  # Z[l] -> processor Pl is used

# Objective function: Minimize the number of processors
model.setObjective(gp.quicksum(Z[l] for l in range(1, m + 1)), GRB.MINIMIZE)

# Constraints
M = n + 1  # Large number for constraints

# [C1] A task is always mapped to exactly one processor
for i in range(1, n + 1):
    model.addConstr(gp.quicksum(X[i, l] for l in range(1, m + 1)) == 1, name=f"C1_task_{i}")

# [C2] (m, k) constraint is satisfied for any window of ki jobs
for i, task in enumerate(tasks, start=1):
    ei, pi, mi, ki = task
    for z in range(1, ni[i - 1] - ki + 2):  # Window positions
        model.addConstr(gp.quicksum(Y[i, j] for j in range(z, z + ki)) >= mi, name=f"C2_task_{i}_window_{z}")

# [C3] All accepted jobs mapped to a processor must be feasible to be scheduled by EDF
time_points = sorted({(j - 1) * task[1] for i, task in enumerate(tasks, start=1) for j in range(1, ni[i - 1] + 1)} |
                     {j * task[1] for i, task in enumerate(tasks, start=1) for j in range(1, ni[i - 1] + 1)})

for l in range(1, m + 1):
    for t1 in time_points:
        for t2 in time_points:
            if t2 > t1:
                model.addConstr(
                    gp.quicksum(X[i, l] * Y[i, j] * tasks[i - 1][0] for i in range(1, n + 1) for j in range(1, ni[i - 1] + 1)
                                if (j - 1) * tasks[i - 1][1] >= t1 and j * tasks[i - 1][1] <= t2) <= t2 - t1,
                    name=f"C3_proc_{l}_interval_{t1}_{t2}"
                )

# [Additional Constraints]
for l in range(1, m + 1):
    model.addConstr(gp.quicksum(X[i, l] for i in range(1, n + 1)) <= M * Z[l], name=f"C4_proc_{l}_usage")
    model.addConstr(Z[l] <= gp.quicksum(X[i, l] for i in range(1, n + 1)), name=f"C5_proc_{l}_assignment")

# Optimize the model
model.optimize()

# Output the results
if model.status == GRB.OPTIMAL:
    print(f"Optimal number of processors: {model.objVal}")
    for i in range(1, n + 1):
        for l in range(1, m + 1):
            if X[i, l].x > 0.5:
                print(f"Task {i} is assigned to Processor {l}")
    for i in range(1, n + 1):
        for j in range(1, ni[i - 1] + 1):
            if Y[i, j].x > 0.5:
                print(f"Job {j} of Task {i} is accepted")
else:
    print("No optimal solution found")
