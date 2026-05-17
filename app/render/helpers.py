import random
import re

from asyncssh import SSHServerProcess

from app.backend.colors import *

ANSI_RE = re.compile(r'\x1b\[[0-9;]*m')
REQUIRED_WIDTH = 64
QUOTES = [
    "Could Be SHITDOKU, by the Way...",
    "Finally, It's Here!",
    "Buy me some Frogs for Breakfast",
    "Nevertheless, Moreover",
    "TUIdoku 10.0.4 BETA",
    "Based on my Passion",
    f"Now try {red('HARD')} Mode",
    "My Hardest Is Tendo",
    "Back for More?",
    "Quite simple, ain't it?",
    "sudoku rm -rf /*",
    "Oh, I missed the point"
]
DIFFICULTIES: dict[int, str] = {
    0: "Easy",
    1: "Medium",
    2: "Hard",
    3: "WalDiy"
}

def visible_len(text: str) -> int:
    return len(ANSI_RE.sub('', text))

def rendered_line_count(text: str) -> int:
    if not text:
        return 0
    return text.count("\n") + 1

def center_visible(text: str, width: int):
    outer_padding = max(0, width - visible_len(text))
    left_outer = outer_padding // 2
    right_outer = outer_padding - left_outer

    return " " * left_outer + text + " " * right_outer

def center_multiline(text: str, width: int, max_width: int):
    line = ""
    lines = []
    for word in text.split():
        if len(line + word) > max_width or len(line + word) > width:
            lines.append(line)
            line = ""
        line += word + " "
    if line != "":
        lines.append(line)

    lines = list(map(lambda l: center_visible(l, width), lines))
    return "\n".join(lines)


def render_title(width: int, sections: list[str]) -> str:
    parts = [center_visible(s, width // len(sections)) for s in sections]
    joined = "".join(parts)

    return bg_white(black(joined + " " * (width - len(joined))))


def render_separator(current_x: int) -> str:
    separator_chars = list("───────┼───────┼───────")
    column_positions = [1, 3, 5, 9, 11, 13, 17, 19, 21]

    separator_chars[column_positions[current_x - 1]] = bg_black(separator_chars[column_positions[current_x - 1]])

    return "".join(separator_chars)


def render_board(
    board: list[list[int]],
    user_cells: list[tuple[int, int]],
    width: int,
    current_x: int,
    current_y: int,
    error_position: tuple[int, int] | None = None,
) -> str:
    lines: list[str] = []
    user_cells_set = set(user_cells)

    if 0 < current_y < 10 and 0 < current_x < 10:
        digit = board[current_y - 1][current_x - 1]
    else:
        digit = 0

    separator = render_separator(current_x)

    for y, row in enumerate(board):
        parts = []

        for x, value in enumerate(row):
            position = (x + 1, y + 1)
            cell = str(value) if value != 0 else " "

            # Determine background
            if position == error_position:
                cell = bg_red(cell)
            elif position == (current_x, current_y):
                if position in user_cells_set:
                    cell = bg_yellow(cell)
                else:
                    cell = bg_white(cell)
            elif y + 1 == current_y or x + 1 == current_x:
                cell = bg_black(cell)

            # Determine foreground
            if position == error_position:
                cell = black(cell)
            elif position == (current_x, current_y):
                cell = black(cell)
            elif value == digit and digit != 0:
                cell = red(cell)
            elif position in user_cells_set:
                cell = yellow(cell)

            parts.append(cell)

            if x % 3 == 2 and x != 8:
                parts.append(bg_black("│") if y + 1 == current_y else "│")

        ln = " ".join(parts) if y + 1 != current_y else bg_black(" ").join(parts)
        lines.append(ln)

        if y % 3 == 2 and y != 8:
            lines.append(separator)

    new_lines = [center_visible(line, width) for line in lines]

    return "\n".join(new_lines)

def get_quote():
    return random.choice(QUOTES)


def disconnect(process: SSHServerProcess):
    from app.render.handler import clear_client

    clear_client(process)
    process.channel.write("\033[?25h")
    process.exit(0)