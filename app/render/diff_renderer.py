from __future__ import annotations

from io import StringIO

from app.backend.colors import RESET


class _BufferedStdout:
    def __init__(self) -> None:
        self._buffer = StringIO()

    def write(self, text: str) -> None:
        self._buffer.write(text)

    def getvalue(self) -> str:
        return self._buffer.getvalue()


class BufferedProcess:
    def __init__(self, process) -> None:
        self._real_process = process
        self.channel = process.channel
        self.stdout = _BufferedStdout()


class DiffRenderer:
    def __init__(self) -> None:
        self._previous_lines: list[str] = []

    def clear(self, process) -> None:
        self._previous_lines = []
        process.channel.write("\033[2J\033[H")

    async def render(self, process, manager, clear_callback) -> None:
        width, height, _, _ = process.channel.get_terminal_size()
        buffered_process = BufferedProcess(process)

        await manager.render(buffered_process, clear_callback, width, height)

        frame = buffered_process.stdout.getvalue()
        current_lines = frame.split("\n")
        total_lines = max(len(current_lines), len(self._previous_lines), height)
        output: list[str] = []

        for row in range(total_lines):
            previous = self._previous_lines[row] if row < len(self._previous_lines) else ""
            current = current_lines[row] if row < len(current_lines) else ""

            if current == previous:
                continue

            output.append(f"\033[{row + 1};1H{current}{RESET}\033[K")

        if output:
            process.channel.write("".join(output))

        self._previous_lines = current_lines
