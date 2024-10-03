from graphics import Window, Line, Point, Cell, Maze


def main() -> None:
    win = Window(800, 600)
    maze = Maze(Point(10, 10), 10, 10, 20, 20, win)
    maze._break_entrance_and_exit()
    win.wait_for_close()


main()
