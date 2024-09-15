from graphics import Window, Line, Point


def main() -> None:
    win = Window(800, 600)
    line1 = Line(Point(20, 20), Point(40, 40), win.canvas)
    line2 = Line(Point(75, 130), Point(63, 400), win.canvas)
    win.draw_line(line1, "green")
    win.draw_line(line2, "black")
    win.wait_for_close()


main()
