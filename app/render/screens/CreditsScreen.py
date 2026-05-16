from typing import Callable

from asyncssh import SSHServerProcess

from app.backend.structures.Screen import Screen
from app.render.helpers import center_visible
from app.render.logo import render_logo


class CreditsScreen(Screen):
    async def render(self, process: SSHServerProcess, clear: Callable[[SSHServerProcess], None]):
        width, height, _, _ = process.channel.get_terminal_size()

        process.stdout.write(render_logo(width))
        process.stdout.write("\n\n")

        process.stdout.write(center_visible("Some Credits", width))

    async def on_keypress(self, process: SSHServerProcess, key: str | bytes):
        from app.render.screens.MenuScreen import MenuScreen
        return MenuScreen()
