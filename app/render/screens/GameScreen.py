import asyncio
from asyncio import sleep, Task
from time import monotonic
from typing import Callable, Optional

from asyncssh import SSHServerProcess

from app.backend.colors import *
from app.backend.generate import generate_sudoku
from app.backend.structures.Board import Board
from app.backend.structures.Screen import Screen
from app.backend.utils import check_win
from app.render.helpers import center_visible, render_title, render_board, DIFFICULTIES, rendered_line_count

MENU = [
    "View solution",
]


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



class GameScreen(Screen):
    # noinspection PyTypeChecker
    def __init__(self, difficulty: int):
        self.difficulty = difficulty

        if difficulty == 0:
            missing = 20
        elif difficulty == 1:
            missing = 30
        elif difficulty == 2:
            missing = 40
        else:
            missing = 50

        board, answer = generate_sudoku(missing)
        self.board = Board(board)
        self.answer = Board(answer)

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
        self.error_until = 0.0
        self.error_position: tuple[int, int] | None = None

    async def auto_render(self, process):
        while True:
            await asyncio.sleep(1)
            await process._diff_renderer.render(process, process._screen_manager, lambda _: None)

    def get_elapsed_time(self) -> str:
        elapsed = int(monotonic() - self.started_at)

        hours = elapsed // 3600
        minutes = (elapsed % 3600) // 60
        seconds = elapsed % 60

        return f"{hours}:{minutes:02}:{seconds:02}"

    def is_error_active(self) -> bool:
        return monotonic() < self.error_until


    def get_filled_count(self) -> int:
        filled = 0

        for x, y in self.user_cells:
            if self.board.board[y - 1][x - 1] != 0:
                filled += 1

        return filled

    async def render(self, process: SSHServerProcess, clear: Callable[[SSHServerProcess], None]):
        if self.render_task is None:
            real_process = getattr(process, "_real_process", process)
            self.render_task = asyncio.create_task(
                self.auto_render(real_process)
            )

        width, height, _, _ = process.channel.get_terminal_size()

        filled = self.get_filled_count()
        error_active = self.is_error_active()

        header = render_title(width, [
            f"SUDOKU [{DIFFICULTIES[self.difficulty].upper()}]",
            self.get_elapsed_time(),
            f"{filled}/{self.total_cells} FILLED",
        ])
        board = render_board(
            self.board.board,
            self.user_cells,
            width,
            self.x,
            self.y,
            self.error_position if error_active else None,
        )

        margin_top = height // 2 - 14 // 2

        lives_indicator = ""
        for i in range(1, 4):
            lives_indicator += red("♡") if i <= self.lives else grey("♡")
            if i != 3:
                lives_indicator += " "

        error_notice = center_visible(
            bg_red(black(" Wrong number! ")) if error_active else " ",
            width
        )
        status = (
            center_visible(lives_indicator, width) + "\n" +
            center_visible(f"{self.lives} / 3", width) + "\n" +
            error_notice
        )
        menu = render_menu(width, self.y)
        footer = render_title(width, [
            "ROGATKA, 2026",
            "ALL RIGHTS RESERVED",
            "CSAI ONE LOVE"
        ])

        process.stdout.write(header)
        process.stdout.write("\n" * margin_top)
        process.stdout.write(board)
        process.stdout.write("\n\n" + status)
        process.stdout.write("\n\n" + menu)

        used_lines = (
            rendered_line_count(header) +
            margin_top +
            rendered_line_count(board) +
            1 +
            rendered_line_count(status) +
            1 +
            rendered_line_count(menu) -
            4
        )
        remains = max(0, height - used_lines - rendered_line_count(footer))
        process.stdout.write("\n" * remains)
        process.stdout.write(footer)


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
                from app.render.screens.SolutionScreen import SolutionScreen
                if self.render_task is not None:
                    self.render_task.cancel()
                return SolutionScreen(self.answer, self.user_cells)

        if key.isdigit() and int(key) != 0 and (self.x, self.y) in self.user_cells:
            try:
                self.board.place(self.x, self.y, int(key))
                self.error_position = None
                self.error_until = 0.0

                if check_win(self.board.board):
                    await process._diff_renderer.render(process, process._screen_manager, lambda _: None)
                    await sleep(1)
                    from app.render.screens.WinScreen import WinScreen
                    if self.render_task is not None:
                        self.render_task.cancel()
                    return WinScreen()
            except ValueError:
                self.lives -= 1
                self.error_position = (self.x, self.y)
                self.error_until = monotonic() + 0.9
                if self.lives <= 0:
                    await process._diff_renderer.render(process, process._screen_manager, lambda _: None)
                    await sleep(1)
                    from app.render.screens.GameOverScreen import GameOverScreen
                    if self.render_task is not None:
                        self.render_task.cancel()
                    return GameOverScreen()

        return None
