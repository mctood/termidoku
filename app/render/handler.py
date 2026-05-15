import traceback

import asyncssh
from asyncssh import TerminalSizeChanged

from app.backend.structures.ScreenManager import ScreenManager
from app.render.screens.MenuScreen import MenuScreen


def clear_client(process: asyncssh.SSHServerProcess):
    process.channel.write("\033[2J\033[H")

def hide_cursor(process: asyncssh.SSHServerProcess):
    process.channel.write("\033[?25l")


async def handle(process: asyncssh.SSHServerProcess):
    process.channel.set_line_mode(False)

    clear_client(process)
    hide_cursor(process)

    # 2. Опционально: отключаем эхо (чтобы клиент сам не печатал нажатую клавишу)
    # process.channel.set_echo(False)

    manager = ScreenManager(MenuScreen())
    width, height, _, _ = process.channel.get_terminal_size()

    try:

        while True:
            try:
                await manager.render(process, clear_client, width, height)

                char = await process.stdin.read(1)

                if not char:
                    break

                if char == '\x1b':
                    char += await process.stdin.read(2)

                await manager.on_keypress(process, char)
            except TerminalSizeChanged:
                clear_client(process)
                width, height, _, _ = process.channel.get_terminal_size()

                # просто заново рисуем текущий screen
                await manager.render(process, clear_client, width, height)
    except Exception as e:
        traceback.print_exc()

        process.stdout.write("\n\nCRASH\n")
        process.stdout.write(traceback.format_exc())

        await process.stdout.drain()
