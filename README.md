
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
init = [
    ['c3', 'c2', 'c2', 'c1'],
    ['c3', 'c1', 'c3', 'c2'],
    ['c2', 'c3', 'c2', 'c3'],
    ['c1', 'c1', 'c1', 'c1'],
    []
]

# Convert the initial list to the format expected by the Tube class
adjust_tubes = [group_colors(tube) for tube in init]

# Initialize the tubes with the adjusted data and a capacity of 4
tubes = init_tubes(adjust_tubes, 4)

# Solve the puzzle using A* search
solution_path, iterations = a_star_solve(tubes)

# Output the solution path
print("Solution Path:")
for move in solution_path:
    print(move)
print("Iterations: ", iterations)
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

## License

This project is licensed under the MIT License.

## Acknowledgments

Inspired by common puzzle-solving algorithms and the desire to apply A* search to a real-world problem.

---

For any issues or questions, please open an issue in the repository or contact the author.
