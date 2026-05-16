from typing import Callable

from asyncssh import SSHServerProcess

from app.backend.colors import yellow, blue
from app.backend.structures.Screen import Screen
from app.render.helpers import center_visible, get_quote, render_title

from app.render.logo import render_logo
from app.render.screens.CreditsScreen import CreditsScreen
from app.render.screens.DifficultyScreen import DifficultyScreen


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

        self.quote = get_quote()
        self.selected = 0

    async def render(self, process: SSHServerProcess, clear: Callable[[SSHServerProcess], None]):
        width, height, _, _ = process.channel.get_terminal_size()
        clear(process)

        process.stdout.write(render_logo(width))

        render_y = height // 2 - (len(MENU) * 3) // 2 - 12

        process.stdout.write("\n" * render_y)

        for i, text in enumerate(MENU):
            btn = render_button(width, text, BUTTON_WIDTH + 2 if i == self.selected else BUTTON_WIDTH)
            process.stdout.write(yellow(btn) if i == self.selected else btn)

        process.stdout.write("\n\n")
        process.stdout.write(center_visible(self.quote, width))
        process.stdout.write(center_visible(f"tg: {blue('@rogatk')}", width))

        remains = height // 2 - 9
        process.stdout.write("\n" * remains)

        process.stdout.write(render_title(width, [
            "ARROWS - MOVE, ENTER - SELECT",
            "PRESS 'Q' ANYTIME TO EXIT"
        ]))


    async def on_keypress(self, process: SSHServerProcess, key: str | bytes):
        if key == 'q':
            process.exit(0)

        if key == '\x1b[A' and self.selected > 0:
            self.selected -= 1

        if key == '\x1b[B' and self.selected < len(MENU) - 1:
            self.selected += 1

        if key == '\r':
            if self.selected == 0:
                return DifficultyScreen()
            if self.selected == 1:
                return CreditsScreen()
            if self.selected == 2:
                from app.render.handler import clear_client

                clear_client(process)
                process.exit(0)

        return None
