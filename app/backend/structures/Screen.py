from typing import Callable

from asyncssh import SSHServerProcess


class Screen:
    async def on_keypress(self, process: SSHServerProcess, key: str | bytes):
        pass

    async def render(self, process: SSHServerProcess, clear: Callable[[SSHServerProcess], None]):
        pass