import traceback

import asyncssh
from asyncssh import TerminalSizeChanged

from app.backend.structures.ScreenManager import ScreenManager
from app.render.diff_renderer import DiffRenderer
from app.render.screens.MenuScreen import MenuScreen


def clear_client(process: asyncssh.SSHServerProcess):
    renderer = getattr(process, "_diff_renderer", None)
    if renderer is not None:
        renderer.clear(process)
        return

    process.channel.write("\033[2J\033[H")

def hide_cursor(process: asyncssh.SSHServerProcess):
    process.channel.write("\033[?25l")


async def handle(process: asyncssh.SSHServerProcess):
    process.channel.set_line_mode(False)
    process._diff_renderer = DiffRenderer()

    # 2. Опционально: отключаем эхо (чтобы клиент сам не печатал нажатую клавишу)
    # process.channel.set_echo(False)

    manager = ScreenManager(MenuScreen())
    process._screen_manager = manager

    clear_client(process)
    hide_cursor(process)

    width, height, _, _ = process.channel.get_terminal_size()

    try:

        while True:
            try:
                await process._diff_renderer.render(process, manager, lambda _: None)

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
                await process._diff_renderer.render(process, manager, lambda _: None)
    except Exception as e:
        traceback.print_exc()

        process.stdout.write("\n\nCRASH\n")
        process.stdout.write(traceback.format_exc())

        await process.stdout.drain()
