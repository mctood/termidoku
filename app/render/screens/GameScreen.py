from asyncio import sleep
from typing import Callable

from asyncssh import SSHServerProcess

from app.backend.colors import *
from app.backend.generate import generate_sudoku
from app.backend.structures.Board import Board
from app.backend.structures.Screen import Screen
from app.backend.utils import center_visible, check_win
from app.render.screens.GameOverScreen import GameOverScreen

MENU = [
    "Hint",
    "Give up",
]


def render_board(board: list[list[int]], user_cells: list[int], width: int, current_x: int, current_y: int) -> str:
    lines: list[str] = []

    separator = "───────┼───────┼───────"

    for y, row in enumerate(board):
        parts = []

        for x, value in enumerate(row):
            cell = str(value) if value != 0 else " "
            if y + 1 == current_y and x + 1 == current_x:
                cell = black(cell)
                if (x, y) in user_cells:
                    cell = bg_yellow(cell)
                else:
                    cell = bg_magenta(cell)
            if (x, y) in user_cells:
                cell = yellow(cell)


            parts.append(cell)

            if x % 3 == 2 and x != 8:
                parts.append("│")

        lines.append(" ".join(parts))

        if y % 3 == 2 and y != 8:
            lines.append(separator)

    new_lines = [center_visible(line, width) for line in lines]

    return "\n".join(new_lines)

def render_menu(width: int, current_y: int) -> str:
    lines: list[str] = []
    active = current_y - 10

    lines = []
    for i, item in enumerate(MENU):
        inner = center_visible(item, 14)
        if i == active:
            inner = black(bg_magenta(inner))
        lines.append(center_visible(inner, width))

    return "\n".join(lines)


class GameScreen(Screen):
    def __init__(self):
        self.board = Board(generate_sudoku(20))
        self.user_cells = []
        for y, row in enumerate(self.board.board):
            for x, cell in enumerate(row):
                if cell == 0:
                    self.user_cells.append((x, y))
        self.x = 1
        self.y = 1
        self.mode = "board"
        self.lives = 3
        self.lives_red = False

    async def render(self, process: SSHServerProcess, clear: Callable[[SSHServerProcess], None]):
        clear(process)

        width, height, _, _ = process.channel.get_terminal_size()

        process.stdout.write(render_board(self.board.board, self.user_cells, width, self.x, self.y))

        lives_indicator = ""
        for i in range(1, 4):
            lives_indicator += red("♡") if i <= self.lives else grey("♡")
            if i != 3:
                lives_indicator += " "


        process.stdout.write("\n" + center_visible(lives_indicator, width))
        process.stdout.write(center_visible(f"{self.lives} / 3", width))

        process.stdout.write("\n" + render_menu(width, self.y))

        if self.lives == 0:
            process.stdout.write(center_visible(red("You lose!") if self.lives_red else green("You lose!"), width))


    async def on_keypress(self, process: SSHServerProcess, key: str | bytes):
        if key == "q":
            process.exit(0)

        if key == "\x1b[A" and self.y > 1:
            self.y -= 1
            if self.y < 10:
                self.mode = "board"
        if key == "\x1b[B" and self.y < 9 + len(MENU):
            self.y += 1
            if self.y >= 10:
                self.mode = "menu"
        if key == "\x1b[D" and self.x > 1:
            self.x -= 1
        if key == "\x1b[C" and self.x < 9:
            self.x += 1

        if key.isdigit() and int(key) != 0:
            from app.render.handler import clear_client

            try:
                self.board.place(self.x, self.y, int(key))

                if check_win(self.board.board):
                    await self.render(process, clear_client)
                    await sleep(1)
                    from app.render.screens.WinScreen import WinScreen
                    return WinScreen()
            except ValueError:
                if (self.x, self.y) in self.user_cells:
                    self.lives -= 1
                    if self.lives <= 0:
                        for i in range(8):
                            self.lives_red = not self.lives_red
                            await self.render(process, clear_client)
                            await sleep(0.1)
                        return GameOverScreen()

        return None