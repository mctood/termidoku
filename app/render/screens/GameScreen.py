import asyncio
from asyncio import sleep, Task
from time import monotonic
from typing import Callable, Optional

from asyncssh import SSHServerProcess

from app.backend.colors import *
from app.backend.generate import generate_sudoku
from app.backend.structures.Board import Board
from app.backend.structures.Screen import Screen
from app.backend.utils import center_visible, check_win

MENU = [
    "View solution",
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
        inner = center_visible(item, 15)
        if i == active:
            inner = black(bg_magenta(inner))
        lines.append(center_visible(inner, width))

    return "\n".join(lines)

def render_title(width: int, sections: list[str]) -> str:
    parts = [center_visible(s, width // len(sections)) for s in sections]
    joined = "".join(parts)

    return bg_white(black(joined + " " * (width - len(joined))))


class GameScreen(Screen):
    def __init__(self):
        self.board = Board(generate_sudoku(20))
        self.user_cells = []
        for y, row in enumerate(self.board.board):
            for x, cell in enumerate(row):
                if cell == 0:
                    self.user_cells.append((x + 1, y + 1))
        self.x = 1
        self.y = 1
        self.mode = "board"
        self.lives = 3
        self.started_at = monotonic()
        self.total_cells = len(self.user_cells)
        self.render_task: Optional[Task] = None

        print(self.user_cells)

    async def auto_render(self, process, clear):
        while True:
            await asyncio.sleep(1)
            await self.render(process, clear)

    def get_elapsed_time(self) -> str:
        elapsed = int(monotonic() - self.started_at)

        hours = elapsed // 3600
        minutes = (elapsed % 3600) // 60
        seconds = elapsed % 60

        return f"{hours}:{minutes:02}:{seconds:02}"


    def get_filled_count(self) -> int:
        filled = 0

        for x, y in self.user_cells:
            if self.board.board[y][x] != 0:
                filled += 1

        return filled

    async def render(self, process: SSHServerProcess, clear: Callable[[SSHServerProcess], None]):
        if self.render_task is None:
            self.render_task = asyncio.create_task(
                self.auto_render(process, clear)
            )

        clear(process)

        width, height, _, _ = process.channel.get_terminal_size()

        filled = self.get_filled_count()

        process.stdout.write(render_title(width, [
            "SUDOKU [DEFAULT]",
            self.get_elapsed_time(),
            f"{filled}/{self.total_cells} FILLED",
        ]))

        margin_top = height // 2 - 18 // 2
        process.stdout.write("\n" * margin_top)

        process.stdout.write(render_board(self.board.board, self.user_cells, width, self.x, self.y))

        lives_indicator = ""
        for i in range(1, 4):
            lives_indicator += red("♡") if i <= self.lives else grey("♡")
            if i != 3:
                lives_indicator += " "


        process.stdout.write("\n" + center_visible(lives_indicator, width))
        process.stdout.write(center_visible(f"{self.lives} / 3", width))

        process.stdout.write("\n" + render_menu(width, self.y))

        remains = height - margin_top - len(MENU) - 18
        process.stdout.write("\n" * remains)
        process.stdout.write(render_title(width, [
            "ELIZAR S. 2026",
            "ALL RIGHTS RESERVED",
            "CSAI ONE LOVE"
        ]))


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

        if key == "\r" and self.mode == "menu":
            if self.y == 10:
                from app.render.screens.MenuScreen import MenuScreen
                if self.render_task is not None:
                    self.render_task.cancel()
                return MenuScreen()

        if key.isdigit() and int(key) != 0:
            from app.render.handler import clear_client

            try:
                self.board.place(self.x, self.y, int(key))

                if check_win(self.board.board):
                    await self.render(process, clear_client)
                    await sleep(1)
                    from app.render.screens.WinScreen import WinScreen
                    if self.render_task is not None:
                        self.render_task.cancel()
                    return WinScreen()
            except ValueError:
                if (self.x, self.y) in self.user_cells:
                    self.lives -= 1
                    if self.lives <= 0:
                        await self.render(process, clear_client)
                        await sleep(1)
                        from app.render.screens.GameOverScreen import GameOverScreen
                        if self.render_task is not None:
                            self.render_task.cancel()
                        return GameOverScreen()

        return None