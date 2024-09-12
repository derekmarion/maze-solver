from tkinter import Tk, BOTH, Canvas


class Line:
    def __init__(self, point1: tuple, point2: tuple, canvas: Canvas) -> None:
        self.__point1 = point1
        self.__point2 = point2
        self.__canvas = (
            canvas  # Lines are instantiated with the canvas attr of their parent window
        )

    def draw(self, fill_color: str) -> None:
        self.__canvas.create_line(
            self.__point1[0],
            self.__point1[1],
            self.__point2[0],
            self.__point2[1],
            fill=fill_color,
            width=2,
        )


class Window:
    def __init__(self, width: int, height: int) -> None:
        self.__root = Tk()
        self.__root.title = "Maze Solver"
        self.__canvas = Canvas(self.__root, bg="white", height=height, width=width)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    @property
    def canvas(self) -> Canvas:
        return self.__canvas

    def redraw(self) -> None:
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self) -> None:
        self.__running = True

        while self.__running:
            self.redraw()

        print("window closed")

    def close(self) -> None:
        self.__running = False

    def draw_line(self, line: Line, fill_color: str):
        line.draw(fill_color=fill_color)


class Point:
    def __init__(self, x=0, y=0) -> None:
        self.__x = x
        self.__y = y
