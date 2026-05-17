from typing import Callable

from asyncssh import SSHServerProcess

from app.backend.colors import yellow, black, bg_yellow
from app.backend.structures.Screen import Screen
from app.render.helpers import center_visible, DIFFICULTIES, rendered_line_count, disconnect

from app.render.screens.GameScreen import GameScreen



def render_button(full_width: int, text: str, content_width: int):
    top = center_visible(
        "┌─" + "─" * content_width + "─┐",

        full_width
    )

    middle = center_visible(
        "│ "
        + center_visible(text, content_width)
        + " │",

        full_width
    )

    bottom = center_visible(
        "└─"
        + "─" * content_width
        + "─┘",

        full_width
    )

    return top + "\n" + middle + "\n" + bottom


BUTTON_WIDTH = max(len(DIFFICULTIES[di]) for di in DIFFICULTIES) + 3

class DifficultyScreen(Screen):
    def __init__(self):
        super().__init__()
        self.selected = 0

    async def render(self, process: SSHServerProcess, clear: Callable[[SSHServerProcess], None]):
        width, height, _, _ = process.channel.get_terminal_size()
        title = center_visible("Select Difficulty:", width)
        buttons = "\n".join(
            yellow(render_button(width, DIFFICULTIES[di], BUTTON_WIDTH + 2))
            if di == self.selected else
            render_button(width, DIFFICULTIES[di], BUTTON_WIDTH)
            for di in DIFFICULTIES
        )

        render_y = height // 2 - (len(DIFFICULTIES) * 3) // 2 - 2

        process.stdout.write("\n" * render_y)
        process.stdout.write(title + "\n\n")
        process.stdout.write(buttons)
        process.stdout.write("\n\n")

        back_btn = center_visible("Go Back", 13)
        if self.selected == len(DIFFICULTIES):
            back_btn = black(bg_yellow(back_btn))

        process.stdout.write(center_visible(back_btn, width))


    async def on_keypress(self, process: SSHServerProcess, key: str | bytes):
        if key == 'q':
            disconnect(process)

        if key == '\x1b[A' and self.selected > 0:
            self.selected -= 1

        if key == '\x1b[B' and self.selected < len(DIFFICULTIES):
            self.selected += 1

        if key == '\r' and self.selected < len(DIFFICULTIES):
            return GameScreen(difficulty=self.selected)

        if key == '\r' and self.selected == len(DIFFICULTIES):
            from app.render.screens.MenuScreen import MenuScreen

            return MenuScreen()

        return None
