# Weakly-Hard Real-Time Task Scheduling

This project implements different approaches for scheduling weakly-hard real-time tasks using various patterns and algorithms.

## Project Structure

- `ilp.py`: Integer Linear Programming solution using Gurobi optimizer
- `baseline_e_pattern.ipynb`: Implementation using E-pattern scheduling
- `baseline_r_pattern.ipynb`: Implementation using R-pattern scheduling
- `input_parameters.txt`: Input file for ILP solution
- `input.txt`: Input file for baseline pattern implementations

## Prerequisites

- Python 3.x
- Gurobi Optimizer with valid license
- Jupyter Notebook (for running .ipynb files)

## Installation

1. Install required packages:
```bash
pip install -r requirements.txt
```

2. Ensure you have a valid Gurobi license installed

## Input File Formats

### input_parameters.txt (for ILP solution)
First line contains two integers:
- n: number of tasks
- m: number of processors

Following lines contain task parameters (one task per line):
- e: execution time
- p: period
- m: minimum number of jobs that must be executed
- k: window size for (m,k)-firm guarantee

Example:
```
3 2
3 7 2 3
2 5 1 2
2 10 3 4
```

### input.txt (for baseline patterns)
Each line represents a task with space-separated values:
- execution time
- period
- m value
- k value

Example:
```
2 5 3 5
1 3 2 3
4 7 2 4
```

## Running the Programs

### ILP Solution
```bash
python ilp.py
```
This will:
- Read tasks from `input_parameters.txt`
- Solve the scheduling problem using Gurobi
- Output the optimal number of processors and task assignments

### E-Pattern Solution
1. Open `baseline_e_pattern.ipynb` in Jupyter Notebook
2. Ensure `input.txt` is in the same directory
3. Run all cells
The program will output the minimum number of processors required using E-pattern scheduling

### R-Pattern Solution
1. Open `baseline_r_pattern.ipynb` in Jupyter Notebook
2. Ensure `input.txt` is in the same directory
3. Run all cells
The program will output the minimum number of processors required using R-pattern scheduling

## Solution Approaches

### ILP (Integer Linear Programming)
- Uses Gurobi optimizer to find the optimal solution
- Considers all constraints simultaneously
- Provides globally optimal results but may be computationally intensive

### E-Pattern
- Uses Elastic pattern for job acceptance
- Implements first-fit bin packing with EDF scheduling
- Considers e/p ratio for task sorting
- Pattern ensures uniform distribution of mandatory jobs

### R-Pattern
- Uses Regular pattern for job acceptance
- Accepts first m jobs in every window of k jobs
- Implements similar bin packing and EDF scheduling as E-pattern
- Provides more predictable execution pattern

## Output

All implementations output the minimum number of processors required to schedule the given task set while satisfying the (m,k)-firm guarantees.

## Notes

- The ILP solution provides optimal results but may take longer for large task sets
- E-pattern and R-pattern implementations provide faster but potentially sub-optimal solutions
- All implementations ensure that (m,k)-firm guarantees are met for each task