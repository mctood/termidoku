import asyncio
from typing import Callable

from asyncssh import SSHServerProcess

from app.backend.structures.Board import Board
from app.backend.structures.Screen import Screen
from app.render.helpers import render_board, render_title, center_visible


class SolutionScreen(Screen):
    def __init__(self, solution: Board, user_cells: list[tuple[int, int]]) -> None:
        self.solution = solution
        self.user_cells = user_cells

    async def render(self, process: SSHServerProcess, clear: Callable[[SSHServerProcess], None]):

        clear(process)

        width, height, _, _ = process.channel.get_terminal_size()

        process.stdout.write(render_title(width, [
            "SOLUTION",
        ]))

        margin_top = height // 2 - 14 // 2
        process.stdout.write("\n" * margin_top)

        process.stdout.write(render_board(self.solution.board, self.user_cells, width, 0, 0))
        process.stdout.write("\n")
        process.stdout.write(center_visible("Press any key to continue.", width))

        remains = height - margin_top - 16
        process.stdout.write("\n" * remains)
        process.stdout.write(render_title(width, [
            "ROGATKA, 2026",
            "ALL RIGHTS RESERVED",
            "CSAI ONE LOVE"
        ]))


    async def on_keypress(self, process: SSHServerProcess, key: str | bytes):
        from app.render.screens.MenuScreen import MenuScreen

        return MenuScreen()