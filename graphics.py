from tkinter import Tk, BOTH, Canvas
from dataclasses import dataclass
import time
import random


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
    _visited: bool = False

    def __post_init__(self):
        self._center = Point(
            (self._bottom_right.x + self._upper_left.x) / 2,
            (self._upper_left.y + self._bottom_right.y) / 2,
        )

    @property
    def center(self):
        return self._center

    @property
    def has_top_wall(self) -> bool:
        return self._has_top_wall

    @has_top_wall.setter
    def has_top_wall(self, val: bool) -> None:
        self._has_top_wall = val

    @property
    def has_bottom_wall(self) -> bool:
        return self._has_bottom_wall

    @has_bottom_wall.setter
    def has_bottom_wall(self, val: bool) -> None:
        self._has_bottom_wall = val

    @property
    def has_left_wall(self) -> bool:
        return self._has_left_wall

    @has_left_wall.setter
    def has_left_wall(self, val: bool) -> None:
        self._has_left_wall = val

    @property
    def has_right_wall(self) -> bool:
        return self._has_right_wall

    @has_right_wall.setter
    def has_right_wall(self, val: bool) -> None:
        self._has_right_wall = val

    @property
    def visited(self) -> bool:
        return self._visited

    @visited.setter
    def visited(self, val: bool) -> None:
        self._visited = val

    def draw(self) -> None:
        """Renders cell walls on canvas. Draws white line for
        a removed wall to enable apparent re-rendering in case
        of wall deletion"""

        if self._has_left_wall:
            self._canvas.create_line(
                self._upper_left.x,
                self._upper_left.y,
                self._upper_left.x,
                self._bottom_right.y,
                fill="black",
                width=2,
            )
        else:
            self._canvas.create_line(
                self._upper_left.x,
                self._upper_left.y,
                self._upper_left.x,
                self._bottom_right.y,
                fill="white",
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
        else:
            self._canvas.create_line(
                self._upper_left.x,
                self._bottom_right.y,
                self._bottom_right.x,
                self._bottom_right.y,
                fill="white",
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
        else:
            self._canvas.create_line(
                self._bottom_right.x,
                self._bottom_right.y,
                self._bottom_right.x,
                self._upper_left.y,
                fill="white",
                width=2,
            )
        if self._has_top_wall:
            self._canvas.create_line(
                self._upper_left.x,
                self._upper_left.y,
                self._bottom_right.x,
                self._upper_left.y,
                fill="black",
                width=2,
            )
        else:
            self._canvas.create_line(
                self._upper_left.x,
                self._upper_left.y,
                self._bottom_right.x,
                self._upper_left.y,
                fill="white",
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
    _render: bool = True
    _seed: int = None

    def __post_init__(self):
        self._cells = []
        self._create_cells()
        if self._seed:
            pass

    def _create_cells(self):
        for row in range(0, self._num_rows):
            self._cells.append(
                [Cell(_canvas=self._win.canvas) for x in range(0, self._num_cols)]
            )

        if self._render:
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

    def _break_entrance_and_exit(self):
        """Removes top wall of upper left cell and
        bottom wall of lower right cell"""

        maze_entrance = self._cells[0][0]
        maze_exit = self._cells[-1][-1]
        maze_entrance.has_top_wall = False
        maze_exit.has_bottom_wall = False
        self._win.draw_cell(maze_entrance)
        self._win.draw_cell(maze_exit)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            not_visited_cells = {}
            adjacent_cells = {
                "left": (i, j - 1),
                "right": (i, j + 1),
                "down": (i + 1, j),
                "up": (i - 1, j),
            }
            for direction, index in adjacent_cells.items():
                if 0 <= index[0] < len(self._cells) and 0 <= index[1] < len(self._cells[0]) and not self._cells[index[0]][index[1]].visited:
                    not_visited_cells[direction] = index
            if len(not_visited_cells) == 0:
                self._cells[i][j].draw()
                return
            else:
                destination_cell_key = random.choice(list(not_visited_cells.keys()))
                destination_cell_tuple = not_visited_cells[destination_cell_key]
                #  Logic to determine which cell wall to remove
                if destination_cell_key == "left":
                    self._cells[i][j].has_left_wall = False
                    self._cells[destination_cell_tuple[0]][
                        destination_cell_tuple[1]
                    ].has_right_wall = False
                elif destination_cell_key == "right":
                    self._cells[i][j].has_right_wall = False
                    self._cells[destination_cell_tuple[0]][
                        destination_cell_tuple[1]
                    ].has_left_wall = False
                elif destination_cell_key == "up":
                    self._cells[i][j].has_top_wall = False
                    self._cells[destination_cell_tuple[0]][
                        destination_cell_tuple[1]
                    ].has_bottom_wall = False
                elif destination_cell_key == "down":
                    self._cells[i][j].has_bottom_wall = False
                    self._cells[destination_cell_tuple[0]][
                        destination_cell_tuple[1]
                    ].has_top_wall = False
                print(f"Moving {destination_cell_key}")
                self._win.draw_cell(self._cells[i][j])
                self._win.draw_cell(
                    self._cells[destination_cell_tuple[0]][destination_cell_tuple[1]]
                )
                self._win.draw_move(
                    self._cells[i][j],
                    self._cells[destination_cell_tuple[0]][destination_cell_tuple[1]],
                )
                self._break_walls_r(
                    destination_cell_tuple[0], destination_cell_tuple[1]
                )
