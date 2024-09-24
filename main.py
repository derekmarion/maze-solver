from graphics import Window, Line, Point, Cell, Maze


def main() -> None:
    win = Window(800, 600)
    maze = Maze(Point(10, 10), 20, 20, 40, 40, win)
    win.wait_for_close()


main()
