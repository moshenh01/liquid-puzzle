import heapq
import time
import concurrent.futures


class Tube:
    # colors look like [(color, count), (color, count), ...]
    def __init__(self, colors, capacity):
        self.colors = colors
        self.capacity = capacity  # max number of colors in the tube
        self.size = sum([count for color, count in colors])  # number of colors in the tube

    def push(self, color):
        if color is None:
            return False
        if self.size == self.capacity:
            return False
        # if the tube is empty, add the color
        if self.colors and self.colors[-1][0] == color[0]:
            self.colors[-1] = (color[0], self.colors[-1][1] + color[1])
        else:
            # add the color to the tube
            self.colors.append(color)
        self.size += color[1]
        return True

    def pop(self):
        if not self.colors:
            return None
        color = self.colors.pop()
        self.size -= color[1]
        return color

    def peek(self):
        if not self.colors:
            return None
        return self.colors[-1]

    def is_empty(self):
        return self.size == 0

    def is_full(self):
        return self.size == self.capacity

    def __lt__(self, other):
        return self.size < other.size

    def __le__(self, other):
        return self.size <= other.size

    def __eq__(self, other):
        return self.size == other.size

    def __ne__(self, other):
        return self.size != other.size

    def __gt__(self, other):
        return self.size > other.size

    def __ge__(self, other):
        return self.size >= other.size

    def __str__(self):
        return str(self.colors)

    def __repr__(self):
        return str(self.colors)

    def __hash__(self):
        return hash(self.colors)


def init_tubes(adjust_tubes, tube_size):
    tubes = []
    for colors in adjust_tubes:
        reversed_colors = list(reversed(colors))  # Reverse the order of colors
        tube = Tube(reversed_colors, tube_size)
        tubes.append(tube)
    return tubes


def is_solved(tubes):
    for tube in tubes:
        if not tube.is_empty():
            # Check if the tube is not full or contains more than one unique color
            unique_colors = set(color for color, _ in tube.colors)
            if not tube.is_full() or len(unique_colors) != 1:
                return False
    return True


def move(tubes, source, destination, last_move=None):
    if tubes[source].is_empty():
        return -1

    if tubes[destination].is_full():
        return -1
    source_color, source_count = tubes[source].peek()
    if source_color is None:
        return -1

    # Calculate available space in destination tube
    destination_space = tubes[destination].capacity - tubes[destination].size

    if source_count > destination_space:
        return -1
    # Check if the destination tube is empty or the top color is the same as the source color
    if not tubes[destination].is_empty() and tubes[destination].peek()[0] != source_color:
        return -2

        # Avoid moving colors between identical tubes
    if tubes[source].colors == tubes[destination].colors:
        return -1

    # Avoid cyclic moves
    if last_move and last_move == (destination, source):
        return -1

    # Perform the move
    move_color, move_count = tubes[source].pop()
    if tubes[destination].is_empty() or tubes[destination].peek()[0] == move_color:
        tubes[destination].push((move_color, move_count))
    else:
        return -1

    return 0


def heuristic_cost0(tubes):
    misplaced_colors = 0
    bottom_color_count = {}

    for tube in tubes:
        if tube.is_empty():
            continue

        # Count misplaced colors
        for i in range(1, len(tube.colors)):
            if tube.colors[i][0] != tube.colors[i - 1][0]:
                misplaced_colors += 1

        # Analyze bottom-most colors
        bottom_color = tube.colors[0][0]
        if bottom_color in bottom_color_count:
            bottom_color_count[bottom_color] += 1
        else:
            bottom_color_count[bottom_color] = 1

    # Sum of the number of tubes minus one for each bottom color
    bottom_color_moves = sum(count - 1 for count in bottom_color_count.values())

    return misplaced_colors * 10 + bottom_color_moves


def heuristic_cost(tubes,empty_tubes = 50):
    cost = 0

    empty_tube_count = 0

    for tube in tubes:
        if tube.is_empty():
            empty_tube_count += 1
            continue
        top_color = tube.peek()[0]
        total_colors = sum(count for color, count in tube.colors)
        bottom_color = tube.colors[0][0]  # Get the bottom color

        # Calculate the cost of the tube based on the depth of each color group
        # depth_index = 0
        # for color, count in tube.colors:
        #     for _ in range(count):
        #         if color != top_color:
        #             cost += (depth_index + 1) *10  # Depth starts from 1 at the top
        #         depth_index += 1

        # Calculate the cost of the tube based on the number of color groups
        groups = 1
        for i in range(1, len(tube.colors)):
            if tube.colors[i][0] != tube.colors[i - 1][0]:
                groups += 1
        cost += (groups - 1) * 1000

        # Calculate the cost of the tube based on the number of empty spaces
        if not tube.is_full():
            cost += (tube.capacity - tube.size)

        # Calculate the cost of the tube based on the number of distinct colors
        distinct_colors = len(set(color for color, count in tube.colors))
        if distinct_colors > 1:
            cost += (distinct_colors - 1) * 1000

        # Add penalty for not having the required number of empty tubes
        if empty_tube_count < empty_tubes:
            cost += (empty_tubes - empty_tube_count)

    return cost


def precheck_move(tubes, source, destination, last_move=None):
    if tubes[source].is_empty() or tubes[destination].is_full():
        return False

    source_color, source_count = tubes[source].peek()
    if source_color is None:
        return False

    destination_space = tubes[destination].capacity - tubes[destination].size

    if source_count > destination_space:
        return False

    if not tubes[destination].is_empty() and tubes[destination].peek()[0] != source_color:
        return False

    if tubes[source].colors == tubes[destination].colors:
        return False

    if last_move and last_move == (destination, source):
        return False

    return True


def get_neighbors(tubes, last_move=None):
    neighbors = []
    num_tubes = len(tubes)

    for i in range(num_tubes):
        if tubes[i].is_empty() or (tubes[i].is_full() and len(set(color for color, count in tubes[i].colors)) == 1):
            continue

        for j in range(num_tubes):
            if i == j or tubes[j].is_full():
                continue

            if not precheck_move(tubes, i, j, last_move):
                continue

            new_tubes = [Tube(tube.colors[:], tube.capacity) for tube in tubes]
            res = move(new_tubes, i, j, last_move)

            if res == 0:
                neighbor_cost = heuristic_cost(new_tubes)
                neighbors.append((new_tubes, (i, j), neighbor_cost))

    return neighbors


def a_star_solve(tubes):
    initial_state = [Tube(tube.colors[:], tube.capacity) for tube in tubes]
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

        state_key = tuple(tuple(color_count for color_count in tube.colors) for tube in current)
        if state_key in visited:
            continue

        visited.add(state_key)
        # time for each move
        n_start = time.time()
        neighbors = get_neighbors(current, path[-1] if path else None)
        n_end = time.time()
        print("Neighbors time: ", n_end - n_start)

        print("Filtered neighbors: ", len(neighbors))
        for neighbor, move_action, neighbor_cost in neighbors:
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
    init = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [29, 11, 49, 38, 41, 36, 38, 39, 15, 33, 45, 34, 18, 9, 5, 34, 2, 22, 37, 2, 5, 1, 13, 15, 47, 46, 4, 10, 0, 31, 24, 21, 49, 13, 18, 34, 10, 40, 10, 17, 28, 47, 15, 31, 32, 9, 20, 41, 11, 33], [49, 27, 44, 18, 42, 31, 29, 13, 14, 39, 20, 48, 18, 31, 7, 26, 36, 19, 1, 42, 23, 17, 18, 49, 16, 8, 31, 23, 44, 1, 41, 31, 12, 39, 11, 20, 18, 19, 6, 31, 13, 8, 19, 39, 36, 20, 20, 48, 41, 20], [17, 29, 31, 17, 37, 10, 41, 17, 17, 1, 41, 28, 37, 36, 47, 36, 15, 10, 28, 4, 16, 28, 4, 38, 5, 33, 33, 10, 43, 3, 42, 21, 22, 3, 26, 22, 0, 48, 17, 46, 23, 41, 29, 36, 9, 21, 13, 12, 45, 8], [24, 47, 19, 49, 11, 37, 35, 45, 22, 47, 48, 15, 42, 38, 36, 31, 0, 22, 7, 47, 21, 30, 1, 38, 12, 45, 18, 3, 47, 8, 30, 13, 7, 46, 2, 23, 17, 22, 14, 19, 14, 45, 46, 44, 31, 6, 26, 46, 5, 1], [21, 40, 44, 10, 48, 10, 35, 25, 27, 20, 20, 27, 23, 28, 29, 38, 3, 25, 5, 4, 6, 42, 43, 30, 23, 21, 3, 11, 24, 42, 4, 38, 39, 3, 48, 44, 18, 14, 47, 1, 7, 2, 10, 47, 48, 36, 35, 6, 40, 20], [46, 14, 31, 32, 43, 19, 13, 28, 34, 7, 1, 27, 33, 26, 15, 42, 6, 30, 12, 40, 42, 34, 33, 20, 14, 34, 16, 18, 45, 28, 33, 28, 43, 2, 31, 25, 49, 28, 30, 30, 44, 19, 41, 30, 9, 47, 43, 18, 38, 30], [38, 37, 23, 17, 26, 13, 39, 32, 30, 30, 15, 49, 19, 18, 46, 28, 6, 31, 44, 30, 7, 2, 20, 18, 10, 36, 39, 12, 48, 28, 26, 32, 9, 34, 34, 1, 40, 38, 28, 22, 33, 22, 27, 15, 14, 36, 2, 21, 8, 12], [44, 24, 28, 32, 18, 29, 2, 37, 34, 5, 35, 9, 19, 36, 35, 37, 26, 4, 29, 32, 9, 46, 28, 30, 12, 26, 38, 30, 33, 32, 12, 25, 47, 14, 29, 23, 38, 9, 4, 31, 44, 6, 6, 38, 23, 48, 27, 3, 41, 1], [38, 19, 16, 44, 45, 11, 17, 27, 23, 48, 24, 4, 43, 2, 0, 1, 18, 0, 34, 21, 40, 11, 39, 20, 5, 40, 38, 29, 28, 37, 15, 22, 8, 42, 15, 32, 35, 40, 32, 4, 9, 15, 21, 19, 15, 6, 30, 2, 25, 27], [42, 48, 7, 19, 35, 45, 23, 19, 9, 14, 34, 16, 11, 22, 9, 18, 34, 48, 8, 35, 43, 1, 0, 25, 13, 46, 12, 45, 0, 24, 43, 4, 43, 22, 21, 3, 9, 44, 35, 8, 17, 14, 36, 7, 9, 45, 16, 24, 24, 39], [48, 21, 42, 8, 6, 44, 12, 6, 8, 26, 46, 23, 7, 42, 24, 25, 45, 48, 44, 44, 31, 43, 2, 9, 7, 44, 21, 20, 8, 23, 30, 10, 24, 35, 46, 19, 45, 39, 17, 13, 43, 2, 5, 26, 1, 28, 38, 6, 6, 41], [10, 4, 0, 42, 16, 32, 24, 32, 35, 35, 2, 37, 23, 12, 37, 21, 16, 6, 43, 42, 17, 48, 23, 47, 9, 37, 11, 18, 6, 11, 25, 36, 49, 33, 11, 28, 49, 16, 13, 10, 26, 42, 10, 43, 39, 47, 11, 7, 0, 1], [23, 7, 32, 27, 2, 15, 19, 11, 25, 33, 49, 9, 19, 29, 35, 46, 18, 21, 28, 41, 13, 41, 15, 2, 48, 5, 38, 22, 11, 11, 25, 30, 15, 49, 9, 1, 11, 6, 3, 20, 14, 39, 2, 30, 49, 45, 41, 32, 2, 44], [18, 3, 3, 35, 21, 21, 18, 29, 1, 30, 45, 31, 38, 29, 15, 44, 38, 9, 8, 15, 12, 45, 43, 28, 28, 37, 17, 7, 40, 15, 2, 31, 3, 1, 31, 11, 14, 21, 23, 5, 15, 44, 12, 10, 16, 28, 43, 37, 16, 35], [35, 27, 45, 48, 39, 37, 1, 4, 40, 20, 29, 10, 13, 14, 8, 21, 31, 8, 25, 7, 25, 27, 47, 44, 30, 3, 41, 1, 49, 7, 22, 15, 3, 48, 21, 14, 33, 6, 26, 12, 46, 42, 35, 35, 0, 4, 9, 16, 19, 26], [21, 20, 10, 42, 15, 18, 7, 36, 43, 18, 29, 26, 36, 42, 4, 18, 1, 28, 21, 24, 32, 32, 3, 6, 41, 49, 35, 5, 31, 13, 37, 49, 21, 5, 15, 19, 45, 7, 16, 16, 5, 18, 35, 36, 42, 13, 40, 23, 10, 44], [19, 34, 7, 39, 24, 3, 20, 43, 37, 0, 41, 46, 44, 13, 25, 41, 5, 45, 34, 40, 48, 23, 5, 41, 33, 19, 4, 35, 18, 34, 38, 17, 9, 3, 19, 42, 6, 28, 19, 24, 49, 7, 42, 19, 0, 10, 14, 48, 10, 0], [33, 31, 32, 22, 4, 35, 47, 1, 9, 16, 36, 24, 28, 15, 36, 10, 15, 48, 5, 20, 15, 10, 18, 16, 35, 37, 29, 25, 19, 8, 11, 20, 31, 27, 31, 19, 45, 10, 18, 6, 48, 0, 26, 21, 44, 43, 47, 16, 14, 44], [26, 4, 40, 34, 47, 17, 43, 17, 3, 23, 14, 35, 21, 3, 23, 8, 15, 49, 4, 19, 26, 16, 11, 20, 20, 5, 24, 5, 25, 18, 30, 40, 45, 19, 28, 9, 4, 43, 32, 29, 32, 27, 34, 42, 27, 1, 26, 29, 0, 17], [49, 48, 11, 37, 0, 38, 24, 22, 20, 44, 42, 42, 14, 23, 46, 18, 24, 12, 22, 19, 16, 37, 32, 36, 40, 24, 34, 19, 22, 0, 48, 28, 34, 23, 38, 37, 31, 48, 6, 18, 43, 27, 17, 4, 46, 32, 8, 16, 25, 28], [3, 7, 1, 17, 41, 28, 2, 29, 31, 25, 47, 48, 4, 8, 20, 34, 45, 37, 27, 15, 43, 17, 35, 15, 9, 49, 4, 24, 37, 30, 15, 15, 37, 22, 32, 26, 26, 6, 13, 4, 19, 0, 16, 39, 40, 48, 7, 42, 41, 47], [36, 16, 8, 48, 29, 3, 4, 34, 33, 46, 13, 16, 18, 1, 8, 9, 6, 36, 6, 20, 26, 41, 32, 7, 5, 45, 8, 0, 20, 29, 47, 38, 17, 34, 41, 25, 9, 46, 24, 32, 9, 15, 9, 44, 21, 6, 2, 25, 16, 35], [2, 33, 5, 8, 27, 40, 47, 21, 49, 7, 36, 18, 17, 3, 25, 15, 43, 22, 36, 27, 6, 38, 11, 29, 12, 1, 30, 17, 27, 24, 49, 28, 2, 29, 21, 34, 17, 47, 8, 28, 29, 14, 23, 16, 42, 46, 4, 27, 38, 12], [21, 31, 44, 26, 36, 5, 13, 24, 32, 34, 17, 32, 1, 38, 30, 14, 12, 13, 22, 44, 42, 36, 39, 3, 49, 24, 32, 12, 21, 35, 26, 2, 1, 12, 46, 48, 20, 41, 49, 1, 21, 0, 12, 35, 49, 38, 5, 37, 1, 13], [36, 38, 18, 5, 43, 34, 22, 4, 17, 16, 41, 29, 12, 2, 41, 22, 45, 34, 45, 13, 12, 43, 39, 42, 30, 43, 29, 26, 26, 38, 40, 49, 14, 21, 47, 41, 32, 32, 40, 14, 43, 19, 11, 27, 1, 20, 3, 44, 25, 44], [48, 39, 27, 17, 38, 19, 28, 11, 1, 49, 25, 24, 36, 12, 24, 46, 3, 36, 36, 4, 44, 8, 32, 36, 35, 34, 7, 40, 49, 44, 47, 48, 37, 37, 12, 21, 13, 48, 7, 47, 24, 2, 10, 25, 48, 7, 15, 8, 30, 2], [31, 27, 6, 26, 31, 33, 41, 39, 2, 4, 20, 41, 28, 33, 40, 33, 12, 31, 42, 48, 5, 32, 16, 11, 30, 27, 1, 37, 16, 12, 18, 16, 36, 40, 28, 16, 29, 40, 30, 40, 10, 40, 9, 9, 17, 22, 37, 37, 5, 36], [27, 43, 42, 0, 16, 31, 35, 38, 27, 27, 47, 34, 2, 40, 31, 39, 37, 25, 11, 30, 25, 39, 35, 6, 33, 40, 0, 36, 39, 29, 25, 45, 15, 30, 17, 0, 13, 41, 4, 33, 21, 7, 29, 20, 24, 20, 14, 29, 39, 43], [38, 26, 34, 49, 2, 0, 3, 23, 41, 34, 23, 15, 32, 26, 11, 7, 37, 27, 28, 21, 5, 39, 48, 17, 14, 40, 27, 0, 38, 13, 22, 37, 49, 20, 19, 45, 36, 37, 11, 5, 36, 4, 8, 29, 13, 21, 29, 24, 18, 13], [44, 0, 27, 18, 16, 11, 23, 25, 14, 6, 33, 35, 0, 14, 32, 29, 20, 31, 28, 26, 39, 49, 24, 1, 11, 3, 0, 42, 33, 20, 11, 34, 24, 12, 0, 18, 16, 44, 2, 9, 46, 38, 1, 25, 25, 2, 20, 23, 16, 15], [9, 45, 47, 32, 40, 48, 37, 14, 42, 26, 35, 25, 6, 43, 18, 35, 28, 29, 5, 13, 2, 5, 19, 14, 24, 45, 43, 47, 27, 7, 32, 23, 32, 20, 41, 32, 41, 13, 49, 4, 24, 35, 30, 31, 1, 39, 41, 33, 34, 35], [14, 4, 33, 42, 49, 4, 26, 6, 35, 27, 43, 33, 22, 49, 41, 41, 6, 39, 30, 16, 13, 31, 23, 13, 22, 28, 11, 10, 6, 20, 16, 6, 30, 21, 15, 43, 6, 39, 16, 10, 23, 26, 13, 30, 35, 34, 47, 46, 42, 31], [36, 40, 11, 29, 14, 3, 7, 2, 33, 35, 38, 31, 40, 33, 5, 23, 9, 43, 42, 12, 19, 1, 33, 24, 1, 30, 21, 10, 30, 32, 31, 49, 20, 47, 5, 18, 13, 28, 49, 12, 16, 7, 21, 27, 5, 4, 33, 14, 4, 44], [27, 45, 31, 11, 32, 0, 17, 9, 34, 47, 45, 39, 31, 44, 32, 2, 36, 12, 29, 23, 3, 34, 35, 14, 28, 15, 8, 7, 41, 39, 12, 2, 13, 26, 7, 38, 26, 42, 38, 30, 40, 43, 20, 29, 17, 39, 4, 7, 14, 22], [46, 1, 21, 35, 12, 14, 14, 3, 37, 32, 0, 5, 24, 18, 43, 17, 30, 27, 26, 45, 8, 11, 40, 9, 14, 32, 41, 40, 1, 40, 30, 17, 39, 25, 29, 12, 9, 8, 10, 42, 25, 47, 20, 12, 16, 33, 30, 48, 12, 7], [38, 36, 46, 23, 25, 18, 5, 9, 0, 33, 21, 26, 34, 34, 6, 37, 2, 24, 26, 14, 45, 2, 15, 35, 42, 0, 6, 48, 10, 1, 36, 11, 5, 11, 26, 33, 11, 48, 8, 45, 30, 5, 19, 14, 45, 26, 29, 26, 45, 26], [32, 13, 29, 31, 36, 39, 40, 9, 33, 5, 49, 46, 25, 8, 9, 19, 33, 4, 5, 8, 44, 16, 47, 46, 32, 31, 36, 47, 10, 15, 14, 27, 8, 22, 15, 18, 3, 12, 43, 36, 27, 22, 18, 32, 0, 40, 8, 13, 4, 46], [20, 7, 17, 22, 6, 43, 47, 42, 5, 29, 32, 29, 1, 5, 5, 36, 37, 28, 43, 5, 40, 46, 49, 27, 17, 20, 23, 9, 5, 37, 25, 38, 34, 10, 15, 25, 22, 35, 15, 11, 19, 11, 22, 47, 9, 33, 44, 0, 47, 44], [10, 45, 26, 19, 35, 6, 12, 39, 35, 37, 15, 3, 22, 37, 44, 48, 32, 45, 0, 23, 29, 31, 28, 46, 49, 18, 34, 42, 18, 37, 3, 27, 41, 34, 19, 2, 24, 40, 6, 23, 34, 8, 25, 10, 25, 22, 2, 0, 2, 43], [26, 25, 5, 15, 35, 7, 43, 27, 26, 27, 22, 47, 47, 48, 47, 5, 44, 40, 20, 13, 36, 8, 43, 13, 9, 19, 24, 41, 49, 12, 2, 25, 28, 49, 17, 42, 44, 17, 27, 19, 31, 3, 13, 14, 34, 40, 20, 20, 30, 10], [3, 14, 14, 8, 25, 26, 3, 48, 25, 10, 7, 12, 19, 26, 29, 46, 3, 23, 11, 39, 46, 49, 28, 40, 44, 32, 46, 28, 46, 9, 8, 49, 5, 34, 36, 9, 21, 17, 42, 29, 41, 12, 1, 44, 24, 40, 11, 40, 23, 34], [41, 33, 11, 21, 9, 46, 19, 21, 1, 14, 20, 43, 12, 4, 10, 22, 49, 42, 13, 10, 7, 44, 1, 45, 4, 47, 0, 27, 24, 45, 23, 28, 19, 1, 46, 17, 46, 3, 45, 41, 3, 0, 2, 22, 25, 8, 10, 46, 30, 2], [5, 38, 4, 47, 31, 18, 17, 4, 35, 7, 19, 10, 27, 21, 7, 3, 10, 46, 24, 2, 5, 30, 17, 27, 3, 21, 32, 37, 9, 23, 49, 27, 37, 45, 7, 11, 7, 2, 11, 45, 31, 39, 41, 18, 18, 45, 48, 37, 23, 8], [13, 33, 31, 4, 38, 22, 37, 30, 48, 34, 1, 23, 6, 49, 18, 39, 17, 10, 2, 26, 14, 45, 8, 7, 31, 13, 34, 20, 13, 8, 33, 13, 11, 44, 4, 13, 12, 12, 39, 22, 39, 33, 36, 11, 38, 0, 13, 49, 17, 6], [3, 24, 36, 7, 30, 17, 49, 0, 8, 46, 8, 33, 39, 44, 37, 9, 48, 2, 37, 10, 36, 43, 24, 31, 31, 43, 29, 22, 41, 8, 36, 15, 4, 3, 24, 14, 11, 42, 33, 13, 29, 4, 33, 34, 12, 14, 10, 14, 6, 49], [9, 4, 28, 7, 22, 19, 8, 30, 3, 0, 6, 6, 45, 39, 9, 22, 37, 43, 21, 0, 10, 41, 29, 8, 12, 46, 46, 7, 26, 40, 1, 37, 47, 23, 13, 47, 16, 16, 19, 23, 47, 39, 30, 15, 44, 48, 0, 43, 34, 4], [3, 15, 16, 37, 33, 39, 46, 3, 20, 3, 35, 43, 39, 40, 28, 42, 15, 20, 11, 38, 39, 6, 41, 16, 0, 47, 12, 41, 34, 23, 23, 47, 38, 0, 46, 42, 48, 38, 18, 42, 48, 20, 24, 11, 9, 22, 9, 33, 42, 32], [47, 14, 47, 25, 4, 33, 31, 17, 27, 22, 24, 10, 26, 0, 47, 17, 16, 19, 8, 5, 38, 45, 14, 46, 41, 25, 32, 40, 49, 0, 41, 25, 1, 8, 23, 30, 35, 15, 22, 39, 20, 3, 21, 25, 27, 29, 38, 39, 1, 30], [5, 25, 22, 16, 7, 46, 46, 13, 24, 28, 44, 12, 0, 6, 19, 49, 0, 10, 39, 40, 22, 11, 21, 2, 38, 43, 22, 12, 18, 42, 46, 16, 25, 43, 6, 16, 23, 4, 45, 2, 38, 6, 24, 33, 40, 45, 35, 40, 38, 44], [27, 12, 45, 13, 22, 48, 45, 16, 33, 7, 44, 10, 36, 21, 24, 6, 29, 8, 33, 39, 28, 2, 26, 1, 34, 23, 7, 22, 21, 27, 33, 14, 48, 25, 42, 29, 3, 24, 10, 46, 46, 16, 17, 30, 3, 17, 28, 39, 41, 10]]

    adjust_tubes = convert_init_list(init)
    start = time.time()
    tubes = init_tubes(adjust_tubes, 50)
    moves = a_star_solve(tubes)
    end = time.time()
    for move in moves:
        print("Move from", move[0], "to", move[1])

    print("Number of moves: ", len(moves))
    print("Time taken: ", end - start)


if __name__ == '__main__':
    main()
