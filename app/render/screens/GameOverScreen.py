from typing import Callable

from asyncssh import SSHServerProcess

from app.backend.structures.Screen import Screen

class GameOverScreen(Screen):
    async def render(self, process: SSHServerProcess, clear: Callable[[SSHServerProcess], None]):
        process.stdout.write("You Lose!!!\nPress any key to continue...")

    async def on_keypress(self, process: SSHServerProcess, key: str | bytes):
        from app.render.screens.MenuScreen import MenuScreen
        return MenuScreen()