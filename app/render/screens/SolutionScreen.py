import asyncio
from typing import Callable

from asyncssh import SSHServerProcess

from app.backend.structures.Board import Board
from app.backend.structures.Screen import Screen
from app.render.helpers import render_board, render_title, center_visible, rendered_line_count


class SolutionScreen(Screen):
    def __init__(self, solution: Board, user_cells: list[tuple[int, int]]) -> None:
        self.solution = solution
        self.user_cells = user_cells

    async def render(self, process: SSHServerProcess, clear: Callable[[SSHServerProcess], None]):
        width, height, _, _ = process.channel.get_terminal_size()
        header = render_title(width, [
            "SOLUTION",
        ])
        board = render_board(self.solution.board, self.user_cells, width, 0, 0)
        hint = center_visible("Press any key to continue.", width)
        footer = render_title(width, [
            "TERMIDOKU.XYZ",
            "ALL RIGHTS RESERVED",
            "CSAI ONE LOVE"
        ])

        margin_top = height // 2 - 14 // 2
        process.stdout.write(header)
        process.stdout.write("\n" * margin_top)
        process.stdout.write(board)
        process.stdout.write("\n\n" + hint)

        used_lines = (
            rendered_line_count(header) +
            margin_top +
            rendered_line_count(board) +
            1 +
            rendered_line_count(hint) - 2
        )
        remains = max(0, height - used_lines - rendered_line_count(footer))
        process.stdout.write("\n" * remains)
        process.stdout.write(footer)


    async def on_keypress(self, process: SSHServerProcess, key: str | bytes):
        from app.render.screens.MenuScreen import MenuScreen

        return MenuScreen()
