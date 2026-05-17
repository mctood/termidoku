from typing import Callable

from asyncssh import SSHServerProcess

from app.backend.structures.Screen import Screen
from app.render.helpers import center_visible, center_multiline


class NarrowScreen(Screen):
    async def render(self, process: SSHServerProcess, clear: Callable[[SSHServerProcess], None]):
        width, height, _, _ = process.channel.get_terminal_size()
        from app.render.helpers import REQUIRED_WIDTH

        sad_moron = """⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⡀⢀⠀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡠⣤⣒⡮⠿⠒⠒⠊⠑⠘⠋⠓⠻⠭⢕⡦⢄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣀⢴⡿⠓⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠑⠮⣖⠄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣼⣣⠟⠀⠀⠀⠀⠀⡀⠀⠀⠀⢀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠣⣘⢄⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣜⡼⠁⠀⠀⣴⣶⣿⡿⠟⠀⠀⠀⠛⠿⢿⣿⣷⣶⠆⠀⠀⠀⠀⠀⠘⢶⣆⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⡞⡿⠀⠀⠀⠀⠙⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠀⠀⠀⠀⠀⠀⠀⠀⢳⡳⡀⠀⠀⠀⠀⠀
⠀⠀⠀⣰⢹⠃⠀⠀⢀⡖⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⢧⠀⠀⠀⠀⠀
⠀⠀⠀⢹⣾⠀⠀⠀⣿⠂⣀⡠⠤⠤⢀⡀⠀⣠⣀⠤⠤⠤⠄⣀⡀⠀⠀⢀⠀⠀⠀⠀⠀⠈⣿⡄⠀⠀⠀⠀
⠀⠀⠀⢸⣿⠀⠀⠀⣿⣯⣭⣤⣀⠀⠀⠈⠳⣏⣤⣶⣤⡀⠀⠀⠈⠉⢛⡏⠀⠀⠀⠀⠀⠀⣿⡆⠀⠀⠀⠀
⠀⠀⠀⠸⣿⡀⠀⠀⠹⣿⣿⣿⣿⡇⠀⠀⣶⠿⣿⣿⣿⣷⠀⠀⠀⣰⡿⡀⠀⠀⠀⠀⠀⠀⣿⡇⠀⠀⠀⠀
⠀⠀⠀⠀⣿⣷⠀⠀⠀⠱⢍⡻⢭⣵⠴⠚⠁⠀⠯⣻⠭⣥⣤⡶⠾⠋⠀⠀⠀⠀⠀⠀⠀⢠⣿⡇⠀⠀⠀⠀
⠀⠀⠀⢠⢭⠿⡆⠀⠀⠀⠀⠙⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⢿⣤⣤⠀⠀⠀
⠀⠀⢀⠿⠂⢈⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⣷⣎⠀⠺⢆⠀⠀
⠀⢀⡞⠀⠀⠀⢻⣮⡻⣭⣉⣒⠓⠖⠲⠶⠦⠦⠤⠤⠤⠤⠄⠤⠠⠐⠀⠒⠒⢂⣤⣿⣿⣿⠁⠀⠀⠘⣆⠀
⢀⡞⠁⠀⣤⠀⢀⣿⠉⠛⢿⡻⣿⣶⣦⣤⣤⣀⣀⣠⣀⣤⣤⣴⠶⢞⡛⣻⣿⣿⠿⠋⢹⡇⠀⣠⡀⠈⠻⡄
⢸⠁⠀⣾⣿⡆⠈⣿⠀⠀⠀⠈⠙⢫⣽⣾⣯⣿⣿⢹⣯⡝⣶⣬⣶⣾⢻⡝⠋⠀⠀⠀⢹⡇⠀⣿⣿⡄⠀⢻
⠸⡇⠀⣿⠋⠧⢰⡿⠀⠀⠀⠀⠀⠀⠀⠈⠉⠙⠉⠛⠉⠛⠉⠛⠉⠉⠀⠀⠀⠀⠀⠀⠹⢧⡤⠟⣿⡇⠀⣿
⠀⠣⠴⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠷⠤⠏

"""
        lines = sad_moron.split('\n')
        for l in lines:
            process.stdout.write(center_visible(l, width))
            process.stdout.write("\n")

        process.stdout.write(center_multiline(f"The window is too narrow! Terminal width must be at least {REQUIRED_WIDTH} characters.", width, 40))
    
