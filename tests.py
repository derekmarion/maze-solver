import unittest
from graphics import Maze, Point, Window


class Tests(unittest.TestCase):
    win = Window(0, 0)

    def test_maze_create_cells_1(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(Point(0, 0), num_rows, num_cols, 10, 10, _win=self.win, _render=False)
        self.assertEqual(len(m1._cells), num_rows)
        self.assertEqual(len(m1._cells[0]), num_cols)

    def test_maze_create_cells_2(self):
        num_cols = 120
        num_rows = 100
        m1 = Maze(Point(0, 0), num_rows, num_cols, 10, 10, _win=self.win, _render=False)
        self.assertEqual(len(m1._cells), num_rows)
        self.assertEqual(len(m1._cells[0]), num_cols)

    def test_maze_create_cells_3(self):
        num_cols = 1200
        num_rows = 1000
        m1 = Maze(Point(0, 0), num_rows, num_cols, 10, 10, _win=self.win, _render=False)
        self.assertEqual(len(m1._cells), num_rows)
        self.assertEqual(len(m1._cells[0]), num_cols)


if __name__ == "__main__":
    unittest.main()
