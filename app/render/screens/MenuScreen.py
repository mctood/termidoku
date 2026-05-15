from typing import Callable

from asyncssh import SSHServerProcess

from app.backend.colors import yellow
from app.backend.structures.Screen import Screen

from app.backend.utils import center_visible, visible_len
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


MENU = [
    "Play",
    "Credits",
    "Quit"
]

BUTTON_WIDTH = max(len(x) for x in MENU) + 3

class MenuScreen(Screen):
    def __init__(self):
        super().__init__()

        self.selected = 0

    async def render(self, process: SSHServerProcess, clear: Callable[[SSHServerProcess], None]):
        width, height, _, _ = process.channel.get_terminal_size()
        clear(process)

        render_y = height // 2 - (len(MENU) * 3) // 2

        process.stdout.write("\n" * render_y)

        for i, text in enumerate(MENU):
            btn = render_button(width, text, BUTTON_WIDTH + 2 if i == self.selected else BUTTON_WIDTH)
            process.stdout.write(yellow(btn) if i == self.selected else btn)


    async def on_keypress(self, process: SSHServerProcess, key: str | bytes):
        if key == 'q':
            process.exit(0)

        if key == '\x1b[A' and self.selected > 0:
            self.selected -= 1

        if key == '\x1b[B' and self.selected < len(MENU) - 1:
            self.selected += 1

        if key == '\r':
            if self.selected == 0:
                return GameScreen()
            if self.selected == 2:
                from app.render.handler import clear_client

                clear_client(process)
                process.exit(0)

        return None
