import re

ANSI_RE = re.compile(r'\x1b\[[0-9;]*m')


def visible_len(text: str) -> int:
    return len(ANSI_RE.sub('', text))

def center_visible(text: str, width: int):
    outer_padding = max(0, width - visible_len(text))
    left_outer = outer_padding // 2
    right_outer = outer_padding - left_outer

    return " " * left_outer + text + " " * right_outer