from math import ceil
from typing import Callable

from asyncssh import SSHServerProcess

from app.backend.colors import grey, red, bg_yellow
from app.backend.generate import generate_sudoku
from app.backend.structures.Board import Board
from app.backend.structures.Screen import Screen
from app.backend.utils import center_visible


def render_board(board: list[list[int]], width: int, current_x: int, current_y: int) -> str:
    lines: list[str] = []

    separator = "───────┼───────┼───────"

    for y, row in enumerate(board):
        parts = []

        for x, value in enumerate(row):
            cell = str(value) if value != 0 else grey("□")
            cell = grey(bg_yellow(cell)) if y + 1 == current_y and x + 1 == current_x else cell

            parts.append(cell)

            if x % 3 == 2 and x != 8:
                parts.append("│")

        lines.append(" ".join(parts))

        if y % 3 == 2 and y != 8:
            lines.append(separator)

    new_lines = [center_visible(line, width) for line in lines]

    return "\n".join(new_lines)

class GameScreen(Screen):
    def __init__(self):
        self.board = Board(generate_sudoku(20))
        self.x = 1
        self.y = 1

    async def render(self, process: SSHServerProcess, clear: Callable[[SSHServerProcess], None]):
        clear(process)

        width, height, _, _ = process.channel.get_terminal_size()

        process.stdout.write(render_board(self.board.board, width, self.x, self.y))

        process.stdout.write("\n" + center_visible(red("♡ ") + red("♡ ") + grey("♡"), width))
        process.stdout.write(center_visible("2 / 3", width))
    async def on_keypress(self, process: SSHServerProcess, key: str | bytes):
        if key == "q":
            process.exit(0)

        if key == "\x1b[A" and self.y > 1:
            self.y -= 1
        if key == "\x1b[B" and self.y < 9:
            self.y += 1
        if key == "\x1b[D" and self.x > 1:
            self.x -= 1
        if key == "\x1b[C" and self.x < 9:
            self.x += 1

