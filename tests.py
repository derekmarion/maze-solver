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

    def test_break_entrance_and_exit(self):
        num_cols = 120
        num_rows = 100
        m1 = Maze(Point(0, 0), num_rows, num_cols, 10, 10, _win=self.win, _render=False)
        m1._break_entrance_and_exit()
        self.assertIs(m1._cells[0][0].has_top_wall, False)
        self.assertIs(m1._cells[-1][-1].has_bottom_wall, False)
    
    def test_reset_cells_visited(self):
        num_cols = 10
        num_rows = 10
        m1 = Maze(Point(0, 0), num_rows, num_cols, 10, 10, _win=self.win, _render=False)
        m1._break_entrance_and_exit()
        m1._break_walls_r(0, 0)
        m1._reset_cells_visited()
        for i in range(m1._num_rows):
            for j in range(m1._num_cols):
                self.assertIs(m1._cells[i][j].visited, False)


if __name__ == "__main__":
    unittest.main()
