import re

ANSI_RE = re.compile(r'\x1b\[[0-9;]*m')
REQUIRED_WIDTH = 64


def visible_len(text: str) -> int:
    return len(ANSI_RE.sub('', text))

def center_visible(text: str, width: int):
    outer_padding = max(0, width - visible_len(text))
    left_outer = outer_padding // 2
    right_outer = outer_padding - left_outer

    return " " * left_outer + text + " " * right_outer

def check_win(board: list[list[int]]) -> bool:
    win = True
    for row in board:
        for col in row:
            if col == 0:
                win = False
                break
    return win