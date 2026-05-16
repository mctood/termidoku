import random
import re

from app.backend.colors import bg_white, black, bg_yellow, bg_magenta, yellow, red

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
}

def visible_len(text: str) -> int:
    return len(ANSI_RE.sub('', text))

def center_visible(text: str, width: int):
    outer_padding = max(0, width - visible_len(text))
    left_outer = outer_padding // 2
    right_outer = outer_padding - left_outer

    return " " * left_outer + text + " " * right_outer


def render_title(width: int, sections: list[str]) -> str:
    parts = [center_visible(s, width // len(sections)) for s in sections]
    joined = "".join(parts)

    return bg_white(black(joined + " " * (width - len(joined))))


def render_board(board: list[list[int]], user_cells: list[tuple[int, int]], width: int, current_x: int, current_y: int) -> str:
    lines: list[str] = []

    separator = "───────┼───────┼───────"

    for y, row in enumerate(board):
        parts = []

        for x, value in enumerate(row):
            cell = str(value) if value != 0 else " "
            if y + 1 == current_y and x + 1 == current_x:
                cell = black(cell)
                if (x + 1, y + 1) in user_cells:
                    cell = bg_yellow(cell)
                else:
                    cell = bg_magenta(cell)
            if (x + 1, y + 1) in user_cells:
                cell = yellow(cell)


            parts.append(cell)

            if x % 3 == 2 and x != 8:
                parts.append("│")

        lines.append(" ".join(parts))

        if y % 3 == 2 and y != 8:
            lines.append(separator)

    new_lines = [center_visible(line, width) for line in lines]

    return "\n".join(new_lines)

def get_quote():
    return random.choice(QUOTES)