from typing import Callable

from asyncssh import SSHServerProcess

from app.backend.structures.Screen import Screen


class NarrowScreen(Screen):
    async def render(self, process: SSHServerProcess, clear: Callable[[SSHServerProcess], None]):
        clear(process)

        from app.backend.utils import REQUIRED_WIDTH
        process.stdout.write(f"The window is too narrow! Terminal width must be at least {REQUIRED_WIDTH} characters.")
    