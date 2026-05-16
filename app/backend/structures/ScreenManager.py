from app.backend.structures.Screen import Screen
from app.render.helpers import REQUIRED_WIDTH
from app.render.screens.NarrowScreen import NarrowScreen


class ScreenManager:
    current: Screen

    def __init__(self, initial: Screen):
        self.current = initial

    async def render(self, process, clear, width: int, height: int):
        if width < REQUIRED_WIDTH:
            await NarrowScreen().render(process, clear)
            return

        await self.current.render(process, clear)

    async def on_keypress(self, process, char):
        new_screen = await self.current.on_keypress(process, char)

        if new_screen:
            self.current = new_screen
