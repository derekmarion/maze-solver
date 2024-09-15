from tkinter import Tk, BOTH, Canvas
from typing import Any


class Point:
    def __init__(self, x=0, y=0) -> None:
        self._x = x
        self._y = y

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

class Line:
    def __init__(self, point1: Point, point2: Point, canvas: Canvas) -> None:
        self._point1 = point1
        self._point2 = point2
        self._canvas = (
            canvas  # Lines are instantiated with the canvas attr of their parent window
        )

    def draw(self, fill_color: str) -> None:
        self._canvas.create_line(
            self._point1.x,
            self._point1.y,
            self._point2.x,
            self._point2.y,
            fill=fill_color,
            width=2,
        )


class Window:
    def __init__(self, width: int, height: int) -> None:
        self._root = Tk()
        self._root.title = "Maze Solver"
        self._canvas = Canvas(self._root, bg="white", height=height, width=width)
        self._canvas.pack(fill=BOTH, expand=1)
        self._running = False
        self._root.protocol("WM_DELETE_WINDOW", self.close)

    @property
    def canvas(self) -> Canvas:
        return self._canvas

    def redraw(self) -> None:
        self._root.update_idletasks()
        self._root.update()

    def wait_for_close(self) -> None:
        self._running = True

        while self._running:
            self.redraw()

        print("window closed")

    def close(self) -> None:
        self._running = False

    def draw_line(self, line: Line, fill_color: str):
        line.draw(fill_color=fill_color)





class Cell:
    def __init__(
        self,
        has_left_wall: bool,
        has_right_wall: bool,
        has_top_wall: bool,
        has_bottom_wall: bool,
        point1: Point,
        point2: Point,
        window: Window,  # Must be parent Window instance to which the cell belongs
    ) -> None:
        pass
