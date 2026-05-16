RESET = "\033[0m"
FG_RESET = "\033[39m"
BG_RESET = "\033[49m"
BOLD_RESET = "\033[22m"


def _wrap_lines(text: str, start: str, end: str) -> str:
    if "\n" not in text:
        return f"{start}{text}{end}"

    return "\n".join(
        f"{start}{line}{end}"
        for line in text.split("\n")
    )


def _reapply_style(text: str, reset_sequences: tuple[str, ...], start: str) -> str:
    for reset_sequence in reset_sequences:
        text = text.replace(reset_sequence, reset_sequence + start)
    return text


def _reapply_fg_style(text: str, start: str, bold: bool) -> str:
    full_reset = FG_RESET + (BOLD_RESET if bold else "")
    placeholder = "\0FG_RESET_PLACEHOLDER\0"

    text = text.replace(full_reset, placeholder)
    text = text.replace(FG_RESET, FG_RESET + start)
    text = text.replace(placeholder, full_reset + start)

    return text.replace(RESET, RESET + start)


def fg_color(text: str, code: int, bold: bool = True) -> str:
    params = []
    if bold:
        params.append("1")
    params.append(str(code))

    start = f"\033[{';'.join(params)}m"
    end = FG_RESET + (BOLD_RESET if bold else "")

    # If nested foreground styles or full resets appear inside, restore this
    # outer foreground afterwards so the wrapper continues to apply.
    text = _reapply_fg_style(text, start, bold)

    return _wrap_lines(text, start, end)


def bg_color(text: str, code: int) -> str:
    start = f"\033[{code}m"

    # Do the same for nested background styles.
    text = _reapply_style(text, (RESET, BG_RESET), start)

    return _wrap_lines(text, start, BG_RESET)


def color(text: str, code: int, bold: bool = True) -> str:
    return fg_color(text, code, bold)


# foreground
def black(text): return fg_color(text, 30)
def red(text): return fg_color(text, 31)
def green(text): return fg_color(text, 32)
def yellow(text): return fg_color(text, 33)
def blue(text): return fg_color(text, 34)
def magenta(text): return fg_color(text, 35)
def cyan(text): return fg_color(text, 36)
def grey(text): return fg_color(text, 90)


# background (basic)
def bg_black(text): return bg_color(text, 40)
def bg_red(text): return bg_color(text, 41)
def bg_green(text): return bg_color(text, 42)
def bg_yellow(text): return bg_color(text, 43)
def bg_blue(text): return bg_color(text, 44)
def bg_magenta(text): return bg_color(text, 45)
def bg_cyan(text): return bg_color(text, 46)
def bg_white(text): return bg_color(text, 47)


def bg_light_black(text): return bg_color(text, 100)