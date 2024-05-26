import unittest
from unittest import TestCase

import assingment1

from assingment1 import Tube, move, heuristic_cost, get_neighbors, a_star_solve, initialize_tubes_from_list, is_solved


class TestTube(unittest.TestCase):

    def test_push(self):
        tube = Tube(10, [[1, 1, 1], [2, 2, 2]])
        tube.push([2, 2])
        self.assertEqual(tube.groups, [[1, 1, 1], [2, 2, 2, 2, 2]], "Failed to merge with the last group")

        tube = Tube(10, [[1, 1, 1], [2, 2, 2]])
        tube.push([3, 3])
        self.assertEqual(tube.groups, [[1, 1, 1], [2, 2, 2], [3, 3]], "Failed to add as a new group")

        tube = Tube(10, [[1, 1, 1], [2, 2, 2]])
        with self.assertRaises(ValueError) as context:
            tube.push([3, 3, 3, 3, 3])
        self.assertEqual(str(context.exception), "The tube can only contain up to its size limit.")

        tube = Tube(10)
        tube.push([1, 1, 1])
        self.assertEqual(tube.groups, [[1, 1, 1]], "Failed to push to an empty tube")

        tube = Tube(10, [[1, 1, 1], [2, 2, 2, 2, 2]])
        tube.push([2, 2])
        self.assertEqual(tube.groups, [[1, 1, 1], [2, 2, 2, 2, 2, 2, 2]],
                         "Failed to push to the tube at exact size limit")

        tube = Tube(10, [[1, 1], [2, 2], [3, 3]])
        tube.push([3, 3, 3, 3])
        self.assertEqual(tube.groups, [[1, 1], [2, 2], [3, 3, 3, 3, 3, 3]], "Failed to merge multiple groups")

        tube = Tube(10, [[1, 1], [2, 2], [3, 3]])
        tube.push([4, 4])
        self.assertEqual(tube.groups, [[1, 1], [2, 2], [3, 3], [4, 4]], "Failed to add a new group")

    def test_pop(self):
        tube = assingment1.Tube(10, [[1, 1, 1], [2, 2, 2], [3, 3, 3], [4]])

        # Test popping a group
        popped_group = tube.pop()
        self.assertEqual(popped_group, [4])
        self.assertEqual(tube.groups, [[1, 1, 1], [2, 2, 2], [3, 3, 3]])

        # Test popping from an empty tube
        empty_tube = assingment1.Tube(10)
        with self.assertRaises(IndexError) as context:
            empty_tube.pop()
        self.assertEqual(str(context.exception), "Pop from an empty tube.")

    def test_peek(self):
        tube = assingment1.Tube(10, [[1, 1, 1], [2, 2, 2], [3, 3, 3], [4]])

        # Test peeking the top group
        top_group = tube.peek()
        self.assertEqual(top_group, [4])

        # Test peeking an empty tube
        empty_tube = assingment1.Tube(10)
        self.assertEqual(empty_tube.peek(), -1)

    def test_is_empty(self):
        tube = assingment1.Tube(10, [[1, 1, 1], [2, 2, 2], [3, 3, 3], [4]])

        # Test is_empty method
        self.assertFalse(tube.is_empty())

        empty_tube = assingment1.Tube(10)
        self.assertTrue(empty_tube.is_empty())

    def test_is_full(self):
        tube = assingment1.Tube(10, [[1, 1, 1], [2, 2, 2], [3, 3, 3]])

        # Test is_full method (should not be full)
        self.assertFalse(tube.is_full())

        full_tube = assingment1.Tube(10, [[1] * 10])
        self.assertTrue(full_tube.is_full())

    def test_equality(self):
        tube1 = assingment1.Tube(10, [[1, 1, 1], [2, 2, 2], [3, 3, 3]])
        tube2 = assingment1.Tube(10, [[1, 1, 1], [2, 2, 2], [3, 3, 3]])
        tube3 = assingment1.Tube(10, [[4, 4, 4]])

        # Test equality
        self.assertEqual(tube1, tube2)
        self.assertNotEqual(tube1, tube3)

    def test_comparison(self):
        tube1 = assingment1.Tube(10, [[1, 1, 1], [2, 2, 2]])
        tube2 = assingment1.Tube(10, [[1, 1, 1], [2, 2, 2], [3, 3, 3]])

        # Test comparison
        self.assertLess(tube1, tube2)
        self.assertGreater(tube2, tube1)

    def test_hash(self):
        tube1 = assingment1.Tube(10, [[1, 1, 1], [2, 2, 2], [3, 3, 3]])
        tube_set = {tube1}

        # Test hash method and set membership
        self.assertIn(tube1, tube_set)


class TestInitialize(unittest.TestCase):
    def test_group_colors(self):
        # Test an empty list
        self.assertEqual(assingment1.group_colors([]), [])

        # Test a list with a single group
        self.assertEqual(assingment1.group_colors([1, 1, 1]), [[1, 1, 1]])

        # Test a list with multiple groups
        self.assertEqual(assingment1.group_colors([1, 1, 2, 2, 2, 3, 3, 3, 4]), [[1, 1], [2, 2, 2], [3, 3, 3], [4]])

        # Test a list with alternating colors
        self.assertEqual(assingment1.group_colors([1, 2, 1, 2]), [[1], [2], [1], [2]])

        # Test a list with non-consecutive repeated colors
        self.assertEqual(assingment1.group_colors([1, 1, 2, 3, 3, 2, 2]), [[1, 1], [2], [3, 3], [2, 2]])


class Test(TestCase):
    def test_initialize_tubes_from_list(self):
        # Test initializing tubes from an empty list
        tubes = assingment1.initialize_tubes_from_list(10, [])
        self.assertEqual(tubes, [])

        # Test initializing tubes with a single tube
        tubes = assingment1.initialize_tubes_from_list(10, [[1, 1, 1, 2, 2, 2, 3, 3, 3, 4]])
        expected_tube = assingment1.Tube(10, [[1, 1, 1], [2, 2, 2], [3, 3, 3], [4]])
        self.assertEqual(tubes[0], expected_tube)

        # Test initializing tubes with multiple tubes
        init_list = [
            [1, 1, 1, 2, 2, 2, 3, 3, 3, 4],
            [4, 4, 5, 5, 5],
            [6],
            [7, 7, 7, 7, 8, 8],
            [9, 9, 9, 9, 9]
        ]
        tubes = assingment1.initialize_tubes_from_list(10, init_list)
        expected_tubes = [
            assingment1.Tube(10, [[1, 1, 1], [2, 2, 2], [3, 3, 3], [4]]),
            assingment1.Tube(10, [[4, 4], [5, 5, 5]]),
            assingment1.Tube(10, [[6]]),
            assingment1.Tube(10, [[7, 7, 7, 7], [8, 8]]),
            assingment1.Tube(10, [[9, 9, 9, 9, 9]])
        ]
        self.assertEqual(tubes, expected_tubes)


class Test_move(TestCase):
    def test_move(self):
        # Initialize tubes
        tube0 = Tube(10, [[1, 1, 1], [2, 2, 2], [3, 3, 3], [4]])
        tube1 = Tube(10, [[5, 5], [6, 6, 6]])
        tube2 = Tube(10, [])
        tube3 = Tube(10, [[7, 7, 7, 7], [8, 8]])
        tube4 = Tube(10, [[9, 9, 9, 9, 9, 9, 9, 9, 9, 9]])
        tube5 = Tube(10, [[1, 1, 1], [2, 2, 2], [3, 3, 3]])
        tube6 = Tube(10, [])
        tubes = [tube0, tube1, tube2, tube3, tube4, tube5, tube6]

        # Test moving from a non-empty tube to an empty tube
        result = move(tubes, 0, 2)
        self.assertEqual(result, 0, "successes to move from a non-empty tube to an empty tube")
        self.assertEqual(tubes[0].groups, [[1, 1, 1], [2, 2, 2], [3, 3, 3]])
        self.assertEqual(tubes[2].groups, [[4]])
        result = move(tubes, 2, 0)  # Move the group back to tube0
        self.assertEqual(result, -2, "failed to move the group back to tube0")

        print(tubes[2].groups)
        # Test moving from an empty tube
        result = move(tubes, 6, 1)
        self.assertEqual(result, -1, "Failed to handle moving from an empty tube")

        # Test moving to a full tube
        result = move(tubes, 1, 0)
        self.assertEqual(result, -1, "Failed to handle moving to a full tube")

        # Test moving between non-empty tubes
        result = move(tubes, 1, 3)
        self.assertEqual(result, -2, "failed not the same color")
        self.assertEqual(tubes[1].groups, [[5, 5], [6, 6, 6]])
        self.assertEqual(tubes[3].groups, [[7, 7, 7, 7], [8, 8]])

        # move from a homogeneous tube to a non-empty tube
        result = move(tubes, 4, 2)
        self.assertEqual(result, -1, "Failed to move from a homogeneous tube to a non-empty tube")

        # move from a almost full tube to a almost full tube
        result = move(tubes, 1, 5)
        self.assertEqual(result, -1, "Failed to move from a almost full tube to a almost full tube")
        result = move(tubes, 5, 1)


class Test_heuristic(TestCase):
    def test_heuristic_cost(self):
        # Test heuristic cost for an empty tube
        tube1 = Tube(10, [])
        tubes = [tube1]
        self.assertEqual(heuristic_cost(tubes), 0, "calculate cost for an empty tube")

        # Test heuristic cost for a tube with a single group
        tube2 = Tube(10, [[1, 1, 1]])
        tubes = [tube2]  # basically 10 - 3 = 7, 3 = size of the group
        self.assertEqual(heuristic_cost(tubes), 7, " calculate cost for a tube with a single group OF 3")

        # Test heuristic cost for a tube with multiple groups of the same color
        tube3 = Tube(10, [[1, 1, 1], [1, 1, 1]])
        tubes = [tube3]
        self.assertEqual(heuristic_cost(tubes), 4,
                         " calculate cost for a tube with multiple groups of the same color")

        # Test heuristic cost for a tube with different colors
        tube4 = Tube(10, [[1, 1, 1], [2, 2], [3]])
        tubes = [tube4]
        expected_cost_depth = 20
        expected_cost_groups = 2  # two different grop from the top
        expected_cost_empty = 4  # 4 empty spaces
        expected_cost_colors = 2  # 2 distinct colors
        expected_cost = expected_cost_depth + expected_cost_groups + expected_cost_empty + expected_cost_colors
        self.assertEqual(heuristic_cost(tubes), expected_cost,
                         " calculate cost for a tube with different colors")

        # Test heuristic cost for a mix of empty and non-empty tubes
        tube5 = Tube(10, [[4, 4, 4], [5, 5, 5]])
        tubes = [tube1, tube2, tube5]
        expected_cost_depth = 16
        expected_cost_groups = 1  # one different grop from the top
        expected_cost_empty = 4  # 4 empty spaces
        expected_cost_colors = 1  # 1 distinct colors
        expected_cost = expected_cost_depth + expected_cost_groups + expected_cost_empty + expected_cost_colors
        self.assertEqual(heuristic_cost(tubes), expected_cost,
                         "Failed to calculate cost for a mix of empty and non-empty tubes")

        # Test heuristic cost for a fully filled homogeneous tube
        tube7 = Tube(10, [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])
        tubes = [tube7]
        expected_cost_depth = 0  # No cost since it's homogeneous
        expected_cost_groups = 0  # No changes from the top group
        expected_cost_empty = 0  # No empty spaces
        expected_cost_colors = 0  # No additional distinct colors
        expected_cost = expected_cost_depth + expected_cost_groups + expected_cost_empty + expected_cost_colors
        self.assertEqual(heuristic_cost(tubes), expected_cost,
                         "Failed to calculate cost for a fully filled homogeneous tube")

        # Test heuristic cost for a partially filled homogeneous tube
        tube8 = Tube(10, [[2, 2, 2, 2, 2]])
        tubes = [tube8]
        expected_cost_depth = 0  # No cost since it's homogeneous
        expected_cost_groups = 0  # No changes from the top group
        expected_cost_empty = 5  # Five empty spaces
        expected_cost_colors = 0  # No additional distinct colors
        expected_cost = expected_cost_depth + expected_cost_groups + expected_cost_empty + expected_cost_colors
        self.assertEqual(heuristic_cost(tubes), expected_cost,
                         "Failed to calculate cost for a partially filled homogeneous tube")

        # Test heuristic cost for a complex tube configuration
        tube9 = Tube(10, [[3, 3], [5, 5, 5, 5, 5]])
        tubes = [tube9]
        expected_cost_depth = 5
        expected_cost_groups = 1  # Two changes from the top group
        expected_cost_empty = 3  # Four empty spaces
        expected_cost_colors = 1  # Two additional distinct colors
        expected_cost = expected_cost_depth + expected_cost_groups + expected_cost_empty + expected_cost_colors
        self.assertEqual(heuristic_cost(tubes), expected_cost,
                         "Failed to calculate cost for a complex tube configuration")
        # Test heuristic cost for a complex tube configuration
        tube9 = Tube(10, [[5, 5, 5, 5, 5], [3, 3]])
        tubes = [tube9]
        expected_cost_depth = 20
        expected_cost_groups = 1  # Two changes from the top group
        expected_cost_empty = 3  # Four empty spaces
        expected_cost_colors = 1  # Two additional distinct colors
        expected_cost = expected_cost_depth + expected_cost_groups + expected_cost_empty + expected_cost_colors
        self.assertEqual(heuristic_cost(tubes), expected_cost,
                         "Failed to calculate cost for a complex tube configuration")

        # very variant in colors
        tube10 = Tube(10, [[2], [7], [1], [2], [6], [4], [5], [6], [4], [8]])
        tubes = [tube10]
        expected_cost_depth = 54
        expected_cost_groups = 9  # 9 changes from the top group
        expected_cost_empty = 0  # 1 empty spaces
        expected_cost_colors = 6  # 7 additional distinct colors
        expected_cost = expected_cost_depth + expected_cost_groups + expected_cost_empty + expected_cost_colors
        self.assertEqual(heuristic_cost(tubes), expected_cost,
                         "Failed to calculate cost for a complex tube configuration")


class Test_get_neighbors(TestCase):
    def test_get_neighbors(self):
        # Test case with one tube
        tube1 = Tube(10, [[1, 1, 1]])
        tubes = [tube1]
        neighbors = get_neighbors(tubes)
        self.assertEqual(len(neighbors), 0, "Failed to handle single tube case")

        # Test case with multiple tubes and possible moves
        tube2 = Tube(10, [[1, 1, 1], [2, 2], [3]])
        tube3 = Tube(10, [])
        tube4 = Tube(10, [[4, 4], [5]])
        tubes = [tube2, tube3, tube4]
        neighbors = get_neighbors(tubes)

        expected_moves = [
            ([Tube(10, [[1, 1, 1], [2, 2]]), Tube(10, [[3]]), Tube(10, [[4, 4], [5]])], (0, 1)),
            ([Tube(10, [[1, 1, 1], [2, 2]]), Tube(10, []), Tube(10, [[4, 4], [5], [3]])], (0, 2)),
            ([Tube(10, [[1, 1, 1], [2, 2], [3], [5]]), Tube(10, []), Tube(10, [[4, 4]])], (2, 0)),
            ([Tube(10, [[1, 1, 1], [2, 2], [3]]), Tube(10, [[5]]), Tube(10, [[4, 4]])], (2, 1)),
        ]

        self.assertEqual(len(expected_moves), len(neighbors), "Unexpected number of neighbors")

        for neighbor, expected in zip(neighbors, expected_moves):
            self.assertEqual(neighbor[1], expected[1], f"Unexpected move: {neighbor[1]}")
            self.assertEqual(
                [(tube.size, tube.groups) for tube in neighbor[0]],
                [(tube.size, tube.groups) for tube in expected[0]],
                f"Unexpected neighbor state for move {expected[1]}"
            )

        # Test heuristic cost for neighbors
        for neighbor in neighbors:
            tubes, move_action, cost = neighbor
            expected_cost = heuristic_cost(tubes)
            self.assertEqual(cost, expected_cost, f"Unexpected cost for neighbor {move_action}")


class Test(TestCase):
    def test_a_star_solve(self):
        def test_a_star_solve(self):
            # Test case 1: Simple solvable case
            init_list = [
                [1, 1, 1, 2, 2, 2],
                [2, 2, 1, 1, 1],
                []
            ]
            tubes = initialize_tubes_from_list(6, init_list)
            solution = a_star_solve(tubes)
            expected_solution = [(1, 2), (1, 2), (1, 2), (0, 1), (0, 1), (0, 1)]  # Example expected moves
            self.assertEqual(solution, expected_solution, "Failed to solve simple solvable case")

            # Test case 2: Already solved
            init_list = [
                [1, 1, 1],
                [2, 2, 2],
                []
            ]
            tubes = initialize_tubes_from_list(3, init_list)
            solution = a_star_solve(tubes)
            expected_solution = []
            self.assertEqual(solution, expected_solution, "Failed to recognize already solved case")

            # Test case 3: Complex solvable case
            init_list = [
                [1, 2, 3, 4],
                [2, 3, 4, 1],
                [3, 4, 1, 2],
                [4, 1, 2, 3],
                []
            ]
            tubes = initialize_tubes_from_list(4, init_list)
            solution = a_star_solve(tubes)
            # The exact solution can vary; check if it's a valid solution
            self.assertTrue(is_solved(
                initialize_tubes_from_list(4, [list(group) for group in tubes[i].groups]) for i, j in solution),
                "Failed to solve complex case")


class Test(TestCase):
    def test_is_solved(self):
        # Test case 1: All tubes are empty
        tubes = [Tube(10, []), Tube(10, []), Tube(10, [])]
        self.assertTrue(is_solved(tubes), "Failed to recognize all empty tubes as solved")

        # Test case 2: All tubes are homogeneous
        tubes = [Tube(10, [[1, 1, 1, 1]]), Tube(10, [[2, 2, 2, 2]]), Tube(10, [])]
        self.assertFalse(is_solved(tubes), "Failed to recognize homogeneous tubes as solved")

        # Test case 3: One tube is not homogeneous
        tubes = [Tube(10, [[1, 1, 1, 1]]), Tube(10, [[2, 3, 2, 2]]), Tube(10, [])]
        self.assertFalse(is_solved(tubes), "Failed to recognize non-homogeneous tube as unsolved")

        # Test case 4: Multiple non-homogeneous tubes
        tubes = [Tube(10, [[1, 1, 2, 2]]), Tube(10, [[3, 3, 3, 4]]), Tube(10, [[5, 5, 5, 6]])]
        self.assertFalse(is_solved(tubes), "Failed to recognize multiple non-homogeneous tubes as unsolved")

        # Test case 5: Mixed empty, homogeneous, and non-homogeneous tubes
        tubes = [Tube(10, [[1, 1, 1, 1]]), Tube(10, []), Tube(10, [[3, 3, 4, 4]])]
        self.assertFalse(is_solved(tubes), "Failed to recognize mixed tubes correctly")

        # Test case 6: Single tube, homogeneous
        tubes = [Tube(10, [[1, 1, 1, 1]])]
        self.assertFalse(is_solved(tubes), "Failed to recognize single homogeneous tube as solved")

        # Test case 7: Single tube, non-homogeneous
        tubes = [Tube(10, [[1, 2, 1, 1]])]
        self.assertFalse(is_solved(tubes), "Failed to recognize single non-homogeneous tube as unsolved")
