from unittest import TestCase
from better_model import Tube, init_tubes, is_solved, move, get_neighbors, heuristic_cost


class TestTube(TestCase):
    def setUp(self):
        self.tube = Tube(colors=[(1, 2), (2, 1)], capacity=6)

    def test_push(self):
        self.assertTrue(self.tube.push((2, 2)))  # Push existing color
        self.assertEqual(self.tube.colors, [(1, 2), (2, 3)])

        self.assertTrue(self.tube.push((3, 1)))  # Push new color
        self.assertEqual(self.tube.colors, [(1, 2), (2, 3), (3, 1)])

        self.assertFalse(self.tube.push((4, 1)))  # Push beyond capacity
        self.assertEqual(self.tube.colors, [(1, 2), (2, 3), (3, 1)])

    def test_pop(self):
        self.assertEqual(self.tube.pop(), (2, 1))  # Pop last color
        self.assertEqual(self.tube.colors, [(1, 2)])

        self.assertEqual(self.tube.pop(), (1, 2))  # Pop remaining color
        self.assertEqual(self.tube.colors, [])

        self.assertIsNone(self.tube.pop())  # Pop from empty tube

    def test_peak(self):
        self.assertEqual(self.tube.peak(), (2, 1))  # Peak last color
        self.tube.pop()
        self.assertEqual(self.tube.peak(), (1, 2))  # Peak remaining color
        self.tube.pop()
        self.assertIsNone(self.tube.peak())  # Peak from empty tube

    def test_is_empty(self):
        self.assertFalse(self.tube.is_empty())  # Tube is not empty
        self.tube.pop()
        self.tube.pop()
        self.assertTrue(self.tube.is_empty())  # Tube is empty

    def test_is_full(self):
        self.assertFalse(self.tube.is_full())  # Tube is not full
        self.tube.push((3, 3))
        self.assertTrue(self.tube.is_full())  # Tube is full


class Test_init_tubes(TestCase):
    def test_init_tubes(self):
        tubes = init_tubes([[],
                            [],
                            [],
                            [],
                            [],
                            [],
                            [],
                            [],
                            [],
                            [],
                            [],
                            [],
                            [(4, 3), (2, 1), (17, 1), (7, 1), (1, 1), (4, 1), (12, 1), (6, 1), (18, 1), (0, 1), (9, 1),
                             (0, 1), (5, 1), (8, 1), (4, 1), (10, 1), (11, 1), (3, 1)],
                            [(9, 1), (11, 1), (10, 1), (6, 1), (4, 1), (11, 1), (3, 1), (15, 1), (4, 1), (16, 1),
                             (11, 1), (15, 1), (0, 1), (7, 1), (12, 1), (7, 1), (17, 1), (1, 1), (5, 1), (6, 1)],
                            [(6, 5), (8, 1), (16, 1), (11, 1), (15, 1), (14, 1), (12, 1), (5, 1), (1, 1), (14, 1),
                             (17, 1), (13, 2), (0, 1), (16, 1), (17, 1)],
                            [(7, 1), (19, 1), (9, 1), (6, 1), (7, 1), (17, 1), (13, 2), (16, 1), (2, 1), (7, 1),
                             (14, 1), (3, 1), (1, 1), (18, 1), (11, 1), (1, 1), (3, 1), (11, 1), (1, 1)],
                            [(11, 1), (10, 1), (17, 1), (5, 1), (19, 1), (5, 1), (6, 1), (12, 1), (3, 1), (17, 1),
                             (13, 1), (10, 1), (16, 1), (19, 1), (2, 1), (17, 1), (15, 2), (5, 1), (7, 1)],
                            [(9, 6), (14, 1), (5, 1), (8, 1), (6, 1), (3, 1), (5, 1), (13, 1), (1, 1), (10, 2), (5, 1),
                             (3, 1), (17, 1), (15, 1)],
                            [(17, 1), (4, 1), (13, 1), (19, 1), (12, 2), (8, 1), (19, 1), (3, 1), (18, 1), (12, 1),
                             (4, 1), (17, 1), (12, 1), (7, 1), (13, 1), (10, 1), (14, 1), (2, 1), (3, 1)],
                            [(13, 1), (12, 1), (16, 1), (18, 1), (16, 1), (0, 1), (15, 1), (2, 1), (6, 1), (16, 1),
                             (19, 1), (2, 1), (13, 1), (2, 1), (4, 1), (18, 1), (4, 1), (12, 1), (15, 1), (11, 1)],
                            [(11, 1), (12, 1), (7, 1), (0, 2), (15, 1), (3, 1), (17, 1), (15, 1), (16, 1), (10, 1),
                             (9, 1), (11, 1), (19, 1), (15, 1), (14, 1), (7, 1), (18, 1), (11, 1), (15, 1)],
                            [(13, 2), (4, 1), (19, 1), (6, 1), (10, 1), (16, 1), (15, 1), (1, 1), (14, 1), (5, 1),
                             (7, 1), (0, 1), (18, 1), (12, 1), (8, 1), (1, 1), (5, 1), (1, 1), (4, 1)],
                            [(14, 5), (3, 1), (13, 1), (3, 1), (2, 2), (12, 1), (5, 1), (4, 1), (19, 2), (0, 1),
                             (14, 1), (6, 1), (18, 1), (8, 1)],
                            [(15, 1), (14, 1), (11, 1), (2, 1), (0, 1), (16, 1), (9, 1), (16, 2), (1, 1), (2, 1),
                             (3, 1), (18, 1), (1, 1), (2, 1), (14, 1), (5, 1), (15, 1), (17, 1), (0, 1)],
                            [(2, 1), (12, 1), (1, 1), (8, 1), (0, 1), (19, 1), (10, 1), (14, 1), (9, 1), (18, 1),
                             (9, 1), (1, 1), (10, 1), (16, 1), (13, 1), (9, 1), (8, 1), (18, 2), (7, 1)],
                            [(18, 1), (11, 1), (17, 1), (2, 1), (8, 1), (16, 1), (10, 1), (9, 1), (17, 1), (10, 1),
                             (9, 1), (15, 1), (13, 1), (1, 1), (0, 2), (6, 1), (19, 1), (8, 1), (10, 1)],
                            [(18, 3), (9, 1), (1, 1), (4, 1), (11, 1), (12, 1), (17, 1), (12, 1), (0, 1), (18, 1),
                             (1, 1), (3, 1), (7, 1), (10, 1), (11, 1), (7, 1), (8, 1), (5, 1)],
                            [(19, 1), (18, 1), (12, 1), (0, 1), (11, 1), (8, 3), (5, 1), (10, 1), (2, 2), (7, 1),
                             (10, 1), (19, 2), (12, 1), (15, 1), (6, 1), (1, 1)],
                            [(14, 2), (16, 1), (5, 1), (4, 1), (11, 1), (0, 1), (19, 1), (1, 1), (19, 1), (3, 1),
                             (6, 1), (2, 1), (8, 1), (3, 1), (12, 1), (19, 1), (6, 1), (3, 1), (16, 1)],
                            [(4, 1), (17, 2), (13, 1), (8, 1), (7, 1), (18, 1), (3, 1), (9, 1), (8, 1), (16, 1), (8, 1),
                             (2, 1), (4, 2), (10, 1), (17, 1), (19, 1), (12, 1), (7, 1)],
                            [(0, 1), (5, 1), (14, 1), (13, 2), (16, 1), (6, 1), (9, 1), (3, 1), (2, 1), (19, 1), (3, 1),
                             (11, 1), (1, 1), (0, 1), (7, 1), (4, 1), (6, 1), (14, 1), (0, 1)],
                            [(5, 1), (8, 1), (7, 1), (8, 1), (5, 1), (15, 1), (17, 1), (10, 1), (16, 1), (13, 1),
                             (7, 1), (18, 1), (15, 1), (13, 1), (15, 1), (5, 1), (9, 1), (11, 1), (2, 1), (10, 1)],
                            ], 20)
        self.assertEqual(len(tubes), 32)
        self.assertEqual(tubes[0].colors, [])
        self.assertEqual(tubes[1].colors, [])
        self.assertEqual(tubes[2].colors, [])
        self.assertEqual(tubes[3].colors, [])
        self.assertEqual(tubes[4].colors, [])
        self.assertEqual(tubes[31].colors, [(5, 1), (8, 1), (7, 1), (8, 1), (5, 1), (15, 1), (17, 1), (10, 1), (16, 1),
                                            (13, 1), (7, 1), (18, 1), (15, 1), (13, 1), (15, 1), (5, 1), (9, 1),
                                            (11, 1), (2, 1), (10, 1)])


class TestIsSolved(TestCase):

    def setUp(self):
        self.tube1 = Tube([(1, 5)], 5)  # Full and single color
        self.tube2 = Tube([(2, 5)], 5)  # Full and single color
        self.tube3 = Tube([], 5)  # Empty
        self.tube4 = Tube([(3, 2), (3, 2)], 4)  # Full and single color
        self.tube5 = Tube([(4, 3)], 5)  # Not full
        self.tube6 = Tube([(5, 2), (6, 2)], 4)  # Full but multiple colors

    def test_is_solved(self):
        tubes1 = [self.tube1, self.tube2, self.tube3, self.tube4]
        tubes2 = [self.tube1, self.tube2, self.tube3, self.tube5, self.tube6]

        self.assertTrue(is_solved(tubes1))  # All tubes should meet the condition
        self.assertFalse(is_solved(tubes2))  # tube5 is not full, tube6 has multiple colors


class TestMove(TestCase):

    def setUp(self):
        self.tube1 = Tube([(1, 5)], 5)  # Full and single color
        self.tube2 = Tube([(2, 3)], 3)  # Full and single color
        self.tube3 = Tube([], 5)  # Empty
        self.tube4 = Tube([(3, 2), (3, 2)], 4)  # Full and single color
        self.tube5 = Tube([(4, 3)], 5)  # Not full
        self.tube6 = Tube([(5, 2), (6, 2)], 4)  # Full but multiple colors

    def test_move(self):
        tubes = [self.tube1, self.tube2, self.tube3, self.tube4, self.tube5, self.tube6]

        # Valid move
        result = move(tubes, 1, 2)
        self.assertEqual(result, 0)
        self.assertEqual(tubes[1].colors, [])
        self.assertEqual(tubes[2].colors, [(2, 3)])

        # Invalid move: source is empty
        result = move(tubes, 1, 2)
        self.assertEqual(result, -1)

        # Invalid move: destination is full
        result = move(tubes, 0, 1)
        self.assertEqual(result, -1)

        # Invalid move: source group doesn't fit in destination
        result = move(tubes, 0, 2)
        self.assertEqual(result, -1)

        # Invalid move: colors don't match
        result = move(tubes, 4, 0)
        self.assertEqual(result, -1)


class TestGetNeighbors(TestCase):

    def setUp(self):
        self.tube1 = Tube([(1, 5)], 5)  # Full and single color
        self.tube2 = Tube([(2, 3)], 3)  # Full and single color
        self.tube3 = Tube([], 5)  # Empty
        self.tube4 = Tube([(3, 2), (3, 2)], 4)  # Full and single color
        self.tube5 = Tube([(4, 3)], 5)  # Not full
        self.tube6 = Tube([(5, 2), (6, 2)], 4)  # Full but multiple colors

    def test_get_neighbors(self):
        tubes = [self.tube1, self.tube2, self.tube3, self.tube4, self.tube5, self.tube6]
        neighbors = get_neighbors(tubes)

        # Check the number of neighbors
        expected_neighbors_count = 2  # move from tube 5 to tube 3 and tube 4 to tube 3
        self.assertEqual(len(neighbors), expected_neighbors_count)

        # Check the content of neighbors
        for neighbor_tubes, move, cost in neighbors:
            self.assertIsInstance(neighbor_tubes, list)
            self.assertIsInstance(move, tuple)
            self.assertIsInstance(cost, int)
            self.assertEqual(len(neighbor_tubes), len(tubes))


class Test_h(TestCase):
    def test_heuristic_cost(self):
            state = [
                [(19, 20)], [], [], [], [], [(14, 20)], [(13, 20)], [], [(18, 20)], [(12, 20)],
                [(2, 20)], [(9, 20)], [], [(6, 20)], [(17, 20)], [], [], [], [(3, 20)], [(11, 20)],
                [(15, 20)], [(4, 20)], [(8, 20)], [], [], [], [(5, 20)], [(1, 20)], [(16, 20)], [(7, 20)],
                [(0, 20)], [(10, 20)]
            ]
            tubes = init_tubes(state, 20)

            expected_cost = 20  # Replace this with the expected heuristic cost value based on the state

            actual_cost = heuristic_cost(tubes,12)

            self.assertEqual(actual_cost, expected_cost)

