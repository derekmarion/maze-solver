from tkinter import Tk, BOTH, Canvas
from dataclasses import dataclass
import time


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


@dataclass(kw_only=True)
class Cell:
    _has_left_wall: bool = True
    _has_right_wall: bool = True
    _has_bottom_wall: bool = True
    _has_top_wall: bool = True
    _upper_left: Point = Point(0, 0)
    _bottom_right: Point = Point(0, 0)
    _canvas: Canvas

    def __post_init__(self):
        self._center = Point(
            (self._bottom_right.x + self._upper_left.x) / 2,
            (self._upper_left.y + self._bottom_right.y) / 2,
        )

    @property
    def center(self):
        return self._center

    def draw(self) -> None:
        if self._has_left_wall:
            self._canvas.create_line(
                self._upper_left.x,
                self._upper_left.y,
                self._upper_left.x,
                self._bottom_right.y,
                fill="black",
                width=2,
            )
        if self._has_bottom_wall:
            self._canvas.create_line(
                self._upper_left.x,
                self._bottom_right.y,
                self._bottom_right.x,
                self._bottom_right.y,
                fill="black",
                width=2,
            )
        if self._has_right_wall:
            self._canvas.create_line(
                self._bottom_right.x,
                self._bottom_right.y,
                self._bottom_right.x,
                self._upper_left.y,
                fill="black",
                width=2,
            )
        if self._has_top_wall:
            self._canvas.create_line(
                self._bottom_right.x,
                self._upper_left.y,
                self._upper_left.x,
                self._upper_left.y,
                fill="black",
                width=2,
            )

    def draw_move(self, to_cell: "Cell", undo=False):
        if undo:
            self._canvas.create_line(
                self.center.x,
                self.center.y,
                to_cell.center.x,
                to_cell.center.y,
                fill="gray",
                width=2,
            )
        else:
            self._canvas.create_line(
                self.center.x,
                self.center.y,
                to_cell.center.x,
                to_cell.center.y,
                fill="red",
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

    def draw_cell(self, cell: Cell):
        cell.draw()

    def draw_move(self, cell1: Cell, cell2: Cell, undo=False):
        cell1.draw_move(cell2, undo=undo)


@dataclass
class Maze:
    """Renders a maze and all cells it contains based on cell
    wall length and width and number of rows/columns"""

    _top_left: Point
    _num_rows: int
    _num_cols: int
    _cell_size_x: int
    _cell_size_y: int
    _win: Window
    _cells: list = None

    def __post_init__(self):
        self._cells = []
        self._create_cells()

    def _create_cells(self):
        for row in range(0, self._num_rows):
            self._cells.append(
                [Cell(_canvas=self._win.canvas) for x in range(0, self._num_cols)]
            )

        for i, row in enumerate(self._cells):
            for j, column in enumerate(row):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        # calculate x/y position of cell based on i, j and cell_size
        upper_left_x = self._top_left.x + self._cell_size_x * j
        upper_left_y = self._top_left.y + self._cell_size_y * i
        cell = Cell(
            _upper_left=Point(upper_left_x, upper_left_y),
            _bottom_right=Point(
                upper_left_x + self._cell_size_x, upper_left_y + self._cell_size_y
            ),
            _canvas=self._win.canvas,
        )
        self._cells[i][j] = cell
        self._cells[i][j].draw()
        self._animate()

    def _animate(self):
        self._win.redraw()
        time.sleep(0.05)
