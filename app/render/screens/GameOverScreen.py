from typing import Callable

from asyncssh import SSHServerProcess

from app.backend.structures.Screen import Screen
from app.render.helpers import center_visible


class GameOverScreen(Screen):
    async def render(self, process: SSHServerProcess, clear: Callable[[SSHServerProcess], None]):
        width, height, _, _ = process.channel.get_terminal_size()

        process.stdout.write("\n\n" + center_visible("You Lose!", width))
        process.stdout.write("\n\n" + center_visible("Press any key to continue.", width))

    async def on_keypress(self, process: SSHServerProcess, key: str | bytes):
        from app.render.screens.MenuScreen import MenuScreen
        return MenuScreen()
