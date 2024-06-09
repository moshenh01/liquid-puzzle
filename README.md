
# Tube Puzzle Solver

This project implements a solution to the tube puzzle problem using the A* search algorithm. The objective of the puzzle is to sort colors within tubes such that each tube contains only one color, or is empty.

## Features
- **Tube Class:** Represents a tube with color groups and methods to push and pop colors.
- **Initialization Functions:** Converts initial color configurations into a format suitable for the puzzle.
- **Heuristic Cost Calculation:** Estimates the cost to solve the puzzle from the current state.
- **A* Search Algorithm:** Finds the optimal sequence of moves to solve the puzzle.

## Getting Started

### Prerequisites

- Python 3.x

### Running the Code

1. Clone the repository or download the script.
2. Ensure you have Python installed on your machine.
3. Run the script using a Python interpreter.

### Example Usage

```python
empty = 2
full = 8
size = 8
colors = 8
init = [[1,3,5,4,4,7,6,1],[2,2,0,0,4,3,6,7],
        [2,1,1,4,5,6,0,2],[0,6,6,5,4,7,7,3],
        [3,4,1,0,5,7,4,4],[7,6,2,2,3,1,0,0],
        [7,3,3,1,2,5,5,6],[7,6,5,5,3,2,1,0],[],[]]

adjust_tubes = convert_init_list(init)
tubes = init_tubes(adjust_tubes, 8) //adding the size for each tube
moves, iterations = a_star_solve(tubes)


```

### Code Structure

- **Tube Class:** Handles tube operations like pushing, popping, and peeking at colors.
- **Helper Functions:**
  - `group_colors`: Groups consecutive identical colors.
  - `init_tubes`: Initializes tubes with given configurations and capacity.
  - `is_solved`: Checks if the puzzle is solved.
  - `move`: Executes a move from one tube to another.
  - `heuristic_cost`: Computes the heuristic cost for the current state.
  - `precheck_move`: Checks if a move is valid before executing it.
  - `get_neighbors`: Generates neighboring states for the A* algorithm.
  - `count_empty_tubes`: Counts the number of empty tubes.
  - `a_star_solve`: Executes the A* search algorithm to find the solution.

### Notes

- The code prints the current state, cost, frontier size, visited size, and iteration count during each step of the A* search.
- The solution path and number of iterations are printed after the puzzle is solved.


#### For more usage example look in file "liquid puzzle test examples"


