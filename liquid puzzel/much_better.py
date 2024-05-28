import heapq
import time
import numpy as np

class Tube:
    def __init__(self, colors, capacity):
        self.colors = np.array(colors)
        self.capacity = capacity
        self.size = np.sum(self.colors[:, 1]) if self.colors.size else 0

    def push(self, color):
        if color is None:
            return False
        if self.size == self.capacity:
            return False
        if self.colors.size > 0 and self.colors[-1, 0] == color[0]:
            self.colors[-1, 1] += color[1]
        else:
            self.colors = np.append(self.colors, [color], axis=0)
        self.size += color[1]
        return True

    def pop(self):
        if self.colors.size == 0:
            return None
        color = self.colors[-1]
        self.colors = self.colors[:-1]
        self.size -= color[1]
        return color

    def peek(self):
        return self.colors[-1] if self.colors.size > 0 else None

    def is_empty(self):
        return self.size == 0

    def is_full(self):
        return self.size == self.capacity

    def __str__(self):
        return str(self.colors)

    def __repr__(self):
        return str(self.colors)

    def __hash__(self):
        return hash(tuple(map(tuple, self.colors)))

    def __lt__(self, other):
        return (self.size, self.capacity) < (other.size, other.capacity)

    def __le__(self, other):
        return (self.size, self.capacity) <= (other.size, other.capacity)

    def __eq__(self, other):
        return (self.size, self.capacity) == (other.size, other.capacity)

    def __ne__(self, other):
        return not self == other

    def __gt__(self, other):
        return (self.size, self.capacity) > (other.size, other.capacity)

    def __ge__(self, other):
        return (self.size, self.capacity) >= (other.size, other.capacity)

def init_tubes(adjust_tubes, tube_size):
    tubes = []
    for colors in adjust_tubes:
        # if tube is empty, create an empty tube
        if colors == []:
            reversed_colors = np.empty((0, 2), int)  # Create an empty 2D array with shape (0, 2)
        else:
            reversed_colors = np.array(list(reversed(colors)))  # Reverse the order of colors using NumPy array
        tube = Tube(reversed_colors, tube_size)
        tubes.append(tube)
    return tubes

def is_solved(tubes):
    for tube in tubes:
        if not tube.is_empty():
            unique_colors = set(color for color in tube.colors[:, 0])
            if not tube.is_full() or len(unique_colors) != 1:
                return False
    return True

def move(tubes, source, destination, last_move=None):
    if tubes[source].is_empty() or tubes[destination].is_full():
        return -1

    source_color, source_count = tubes[source].peek()
    destination_space = tubes[destination].capacity - tubes[destination].size

    if source_count > destination_space or (not tubes[destination].is_empty() and tubes[destination].peek()[0] != source_color):
        return -1

    if last_move and last_move == (destination, source):
        return -1

    move_color, move_count = tubes[source].pop()
    tubes[destination].push((move_color, move_count))
    return 0

def heuristic_cost(tubes):
    cost = 0

    for tube in tubes:
        if tube.is_empty():
            continue

        colors = tube.colors
        top_color = colors[-1, 0] if colors.size > 0 else None
        bottom_color = colors[0, 0] if colors.size > 0 else None

        # Calculate the cost of the tube based on the number of color groups
        group_changes = np.sum(colors[1:, 0] != colors[:-1, 0])
        cost += group_changes * 1000

        # Calculate the cost of the tube based on the number of empty spaces
        if not tube.is_full():
            cost += (tube.capacity - tube.size)

        # Calculate the cost of the tube based on the number of distinct colors
        distinct_colors = np.unique(colors[:, 0]).size
        if distinct_colors > 1:
            cost += (distinct_colors - 1) * 1000

    return cost


def get_neighbors(tubes, last_move=None):
    neighbors = []
    num_tubes = len(tubes)

    for i in range(num_tubes):
        if tubes[i].is_empty() or (tubes[i].is_full() and len(np.unique(tubes[i].colors[:, 0])) == 1):
            continue

        for j in range(num_tubes):
            if i == j or tubes[j].is_full():
                continue

            # Create a deep copy only when needed
            new_tubes = [Tube(tube.colors.copy(), tube.capacity) for tube in tubes]
            res = move(new_tubes, i, j, last_move)

            if res == 0:
                neighbor_cost = heuristic_cost(new_tubes)
                neighbors.append((new_tubes, (i, j), neighbor_cost))

    return neighbors


def a_star_solve(tubes):
    initial_state = [Tube(tube.colors.copy(), tube.capacity) for tube in tubes]
    initial_cost = heuristic_cost(initial_state)
    frontier = [(initial_cost, 0, initial_state, [])]
    heapq.heapify(frontier)
    visited = set()

    while frontier:
        h_cost, cost, current, path = heapq.heappop(frontier)
        print("Current state:")
        for i, tube in enumerate(current):
            print(f"Tube {i}: {tube.colors}")
        print("Cost: ", h_cost)
        print("Frontier: ", len(frontier))
        print("Visited: ", len(visited))
        if is_solved(current):
            return path

        state_key = tuple(tuple(map(tuple, tube.colors)) for tube in current)
        if state_key in visited:
            continue
        visited.add(state_key)

        for neighbor, move_action, neighbor_cost in get_neighbors(current, path[-1] if path else None):
            new_path = path + [move_action]
            new_cost = cost + 1
            heapq.heappush(frontier, (neighbor_cost, new_cost, neighbor, new_path))
            if len(frontier) > 10000:
                frontier = heapq.nsmallest(1000, frontier)
                heapq.heapify(frontier)
    return []

def group_colors(colors):
    if not colors:
        return []

    grouped_colors = []
    current_color = colors[0]
    count = 1

    for color in colors[1:]:
        if color == current_color:
            count += 1
        else:
            grouped_colors.append((current_color, count))
            current_color = color
            count = 1

    grouped_colors.append((current_color, count))  # Append the last group
    return grouped_colors


def convert_init_list(init):
    return [group_colors(colors) for colors in init]

def main():
    init = [[], [], [], [], [], [], [], [], [], [], [], [],
            [4, 4, 4, 2, 17, 7, 1, 4, 12, 6, 18, 0, 9, 0, 5, 8, 4, 10, 11, 3],
            [9, 11, 10, 6, 4, 11, 3, 15, 4, 16, 11, 15, 0, 7, 12, 7, 17, 1, 5, 6],
            [6, 6, 6, 6, 6, 8, 16, 11, 15, 14, 12, 5, 1, 14, 17, 13, 13, 0, 16, 17],
            [7, 19, 9, 6, 7, 17, 13, 13, 16, 2, 7, 14, 3, 1, 18, 11, 1, 3, 11, 1],
            [11, 10, 17, 5, 19, 5, 6, 12, 3, 17, 13, 10, 16, 19, 2, 17, 15, 15, 5, 7],
            [9, 9, 9, 9, 9, 9, 14, 5, 8, 6, 3, 5, 13, 1, 10, 10, 5, 3, 17, 15],
            [17, 4, 13, 19, 12, 12, 8, 19, 3, 18, 12, 4, 17, 12, 7, 13, 10, 14, 2, 3],
            [13, 12, 16, 18, 16, 0, 15, 2, 6, 16, 19, 2, 13, 2, 4, 18, 4, 12, 15, 11],
            [11, 12, 7, 0, 0, 15, 3, 17, 15, 16, 10, 9, 11, 19, 15, 14, 7, 18, 11, 15],
            [13, 13, 4, 19, 6, 10, 16, 15, 1, 14, 5, 7, 0, 18, 12, 8, 1, 5, 1, 4],
            [14, 14, 14, 14, 14, 3, 13, 3, 2, 2, 12, 5, 4, 19, 19, 0, 14, 6, 18, 8],
            [15, 14, 11, 2, 0, 16, 9, 16, 16, 1, 2, 3, 18, 1, 2, 14, 5, 15, 17, 0],
            [2, 12, 1, 8, 0, 19, 10, 14, 9, 18, 9, 1, 10, 16, 13, 9, 8, 18, 18, 7],
            [18, 11, 17, 2, 8, 16, 10, 9, 17, 10, 9, 15, 13, 1, 0, 0, 6, 19, 8, 10],
            [18, 18, 18, 9, 1, 4, 11, 12, 17, 12, 0, 18, 1, 3, 7, 10, 11, 7, 8, 5],
            [19, 18, 12, 0, 11, 8, 8, 8, 5, 10, 2, 2, 7, 10, 19, 19, 12, 15, 6, 1],
            [14, 14, 16, 5, 4, 11, 0, 19, 1, 19, 3, 6, 2, 8, 3, 12, 19, 6, 3, 16],
            [4, 17, 17, 13, 8, 7, 18, 3, 9, 8, 16, 8, 2, 4, 4, 10, 17, 19, 12, 7],
            [0, 5, 14, 13, 13, 16, 6, 9, 3, 2, 19, 3, 11, 1, 0, 7, 4, 6, 14, 0],
            [5, 8, 7, 8, 5, 15, 17, 10, 16, 13, 7, 18, 15, 13, 15, 5, 9, 11, 2, 10]]

    adjust_tubes = convert_init_list(init)
    for colors in adjust_tubes:
        print(colors)
    start = time.time()
    tubes = init_tubes(adjust_tubes, 20)
    for tube in tubes:
        print(tube.colors)
    moves = a_star_solve(tubes)
    end = time.time()
    for move in moves:
        print("Move from", move[0], "to", move[1])

    print("Number of moves: ", len(moves))
    print("Time taken: ", end - start)


if __name__ == '__main__':
    main()
