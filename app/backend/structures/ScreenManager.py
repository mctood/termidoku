from app.backend.structures.Screen import Screen


class ScreenManager:
    current: Screen

    def __init__(self, initial: Screen):
        self.current = initial

    async def render(self, process, clear):
        await self.current.render(process, clear)

    async def on_keypress(self, process, char):
        new_screen = await self.current.on_keypress(process, char)

        if new_screen:
            self.current = new_screen
