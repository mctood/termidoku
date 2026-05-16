from typing import Callable

from asyncssh import SSHServerProcess

from app.backend.colors import yellow, blue
from app.backend.structures.Screen import Screen
from app.render.helpers import center_visible, get_quote, render_title, rendered_line_count

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
        logo = render_logo(width)
        buttons = "\n".join(
            yellow(render_button(width, text, BUTTON_WIDTH + 2))
            if i == self.selected else
            render_button(width, text, BUTTON_WIDTH)
            for i, text in enumerate(MENU)
        )
        quote_block = (
            center_visible(self.quote, width) + "\n" +
            center_visible(f"tg: {blue('@rogatk')}", width)
        )
        footer = render_title(width, [
            "ARROWS - MOVE, ENTER - SELECT",
            "PRESS 'Q' ANYTIME TO EXIT"
        ])

        process.stdout.write(logo)

        render_y = height // 2 - (len(MENU) * 3) // 2 - 7

        process.stdout.write("\n" * render_y)
        process.stdout.write(buttons)
        process.stdout.write("\n\n")
        process.stdout.write(quote_block)

        used_lines = (
            rendered_line_count(logo) +
            render_y +
            rendered_line_count(buttons) +
            2 +
            rendered_line_count(quote_block) -
            3
        )
        remains = max(0, height - used_lines - rendered_line_count(footer))
        process.stdout.write("\n" * remains)
        process.stdout.write(footer)


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
