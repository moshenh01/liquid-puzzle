import heapq


class Tube:

    def __init__(self, size, groups=None):
        self.size = size
        if groups is None:
            groups = []
        self.groups = [group for group in groups]

    def push(self, group):
        total_colors = sum(len(g) for g in self.groups)
        if total_colors + len(group) > self.size:
            raise ValueError("The tube can only contain up to its size limit.")

        if self.groups and self.groups[-1][0] == group[0]:
            self.groups[-1] = self.groups[-1] + group  # Merge with the existing group
        else:
            self.groups.append(group)  # Add as a new group

    def pop(self):
        if not self.groups:
            raise IndexError("Pop from an empty tube.")
        return self.groups.pop()

    def peek(self):
        if not self.groups:
            return -1
        return self.groups[-1]

    def is_empty(self):
        return len(self.groups) == 0

    def is_full(self):
        total_colors = sum(len(g) for g in self.groups)
        return total_colors == self.size

    def __eq__(self, other):
        return self.groups == other.groups

    def __lt__(self, other):
        return self.groups < other.groups

    def __hash__(self):
        # Convert groups to a tuple of tuples for hashing
        return hash(tuple(tuple(group) for group in self.groups))


def group_colors(colors):
    if not colors:
        return []

    grouped_colors = []
    current_group = [colors[0]]

    for color in colors[1:]:
        if color == current_group[-1]:
            current_group.append(color)
        else:
            grouped_colors.append(current_group)
            current_group = [color]

    grouped_colors.append(current_group)  # Append the last group
    return grouped_colors


def initialize_tubes_from_list(size, init_list):
    tubes = []
    for colors in init_list:
        # Ensure that colors is a list
        if colors is None:
            colors = []
        grouped_colors = group_colors(colors)
        tube = Tube(size, grouped_colors)
        tubes.append(tube)
    return tubes


def is_solved(tubes):
    for tube in tubes:
        if not tube.is_empty():
            if not tube.is_full() or len(set(color for group in tube.groups for color in group)) != 1:
                return False
    return True


def move(tubes, source, destination):
    if tubes[source].is_empty():
        return -1

    if tubes[source].is_full() and len(set(color for group in tubes[source].groups for color in group)) == 1:
        return -1

    if tubes[destination].is_full():
        return -1

    source_group = tubes[source].peek()
    destination_space = tubes[destination].size - sum(len(g) for g in tubes[destination].groups)
    #
    if len(source_group) > destination_space:
        return -1

    if not tubes[destination].is_empty() and tubes[destination].peek()[0] != source_group[0]:
        return -2

    tubes[destination].push(tubes[source].pop())
    return 0


def heuristic_cost(tubes):
    cost = 0
    for tube in tubes:
        if tube.is_empty():
            continue
        top_color = tube.peek()[0]
        total_colors = sum(len(group) for group in tube.groups)

        # 1. Calculate the cost of the tube based on the depth of each color group
        depth_index = 0
        for group in tube.groups:
            for color in group:
                if color != top_color:
                    cost += (depth_index + 1)  # Depth starts from 1 at the top
                depth_index += 1

        # print("Cost1: ", cost)

        # 2. Calculate the cost of the tube based on the number of color groups
        groups = 1
        for i in range(1, len(tube.groups)):
            if tube.groups[i][0] != tube.groups[i - 1][0]:
                groups += 1
        cost += (groups - 1)
        # print("Cost2: ", cost)

        # 3. Calculate the cost of the tube based on the number of empty spaces
        if not tube.is_full():
            cost += (tube.size - total_colors)
        # print("Cost3: ", cost)

        # 4. Calculate the cost of the tube based on the number of distinct colors
        distinct_colors = len(set(color for group in tube.groups for color in group))
        if distinct_colors > 1:
            cost += distinct_colors - 1
        # print("Cost4: ", cost)
    return cost


def get_neighbors(tubes):
    neighbors = []
    for i in range(len(tubes)):
        if not tubes[i].is_empty() and not (
                tubes[i].is_full() and len(set(color for group in tubes[i].groups for color in group)) == 1):
            for j in range(len(tubes)):
                if i != j and not tubes[j].is_full():
                    new_tubes = [Tube(tube.size, [list(group) for group in tube.groups]) for tube in tubes]

                    # print("move: ", i, j)
                    res = move(new_tubes, i, j)
                    if res == 0:
                        neighbor_cost = heuristic_cost(new_tubes)
                        neighbors.append((new_tubes, (i, j), neighbor_cost))

    return neighbors


def a_star_solve(tubes):
    initial_state = [Tube(tube.size, [list(group) for group in tube.groups]) for tube in tubes]
    initial_cost = heuristic_cost(initial_state)
    frontier = [(initial_cost, initial_cost, 0, initial_state, [])]
    heapq.heapify(frontier)
    visited = set()

    while frontier:
        priority, h_cost, cost, current, path = heapq.heappop(frontier)

        print("Current state:")
        for i, tube in enumerate(current):
            print(f"Tube {i}: {tube.groups}")
        print("Cost: ", h_cost)
        print("Frontier: ", len(frontier))
        print("Visited: ", len(visited))

        if is_solved(current):
            return path

        state_key = tuple(tuple(tuple(group) for group in tube.groups) for tube in current)
        if state_key in visited:
            continue

        visited.add(state_key)

        # Get the neighbors of the current state and add them to the frontier with their costs
        for neighbor, move_action, neighbor_cost in get_neighbors(current):
            new_path = path + [move_action]
            new_cost = cost + 1

            # Adjusting the priority to give more weight to neighbor_cost
            priority = neighbor_cost

            heapq.heappush(frontier, (priority, neighbor_cost, new_cost, neighbor, new_path))
            # Prune the frontier to keep only the 1000 states with the lowest costs
            if len(frontier) > 50000:
                frontier = heapq.nsmallest(1000, frontier)
                heapq.heapify(frontier)

    return []


def main():
    init = [[], [], [], [], [], [4, 4, 6, 1, 9, 5, 3, 3, 8, 7], [2, 9, 8, 7, 3, 2, 1, 4, 0, 0],
            [7, 8, 8, 7, 8, 4, 8, 4, 2, 5],
            [3, 8, 6, 0, 6, 3, 5, 2, 6, 9], [2, 2, 3, 3, 3, 6, 9, 5, 7, 0], [0, 5, 0, 4, 0, 7, 9, 1, 7, 1],
            [2, 7, 1, 2, 6, 4, 5, 6, 4, 8],
            [6, 7, 8, 2, 9, 1, 9, 0, 4, 3], [0, 2, 9, 7, 1, 8, 6, 5, 9, 5], [0, 5, 5, 6, 3, 4, 1, 1, 1, 9]]

    tubes = initialize_tubes_from_list(10, init)
    # print(tubes[11].groups)
    moves = a_star_solve(tubes)

    print("\nMoves:")
    for move in moves:
        print(f"Move color from tube {move[0]} to tube {move[1]}")
    print("moves: ", len(moves))


if __name__ == '__main__':
    main()
