RESET = "\033[0m"

def color(text: str, code: int, bold: bool = True) -> str:
    prefix = "1;" if bold else ""
    return f"\033[{prefix}{code}m{text}{RESET}"


# foreground
def red(text): return color(text, 31)
def green(text): return color(text, 32)
def yellow(text): return color(text, 33)
def blue(text): return color(text, 34)
def magenta(text): return color(text, 35)
def cyan(text): return color(text, 36)
def grey(text): return color(text, 90)


# background (basic)
def bg_black(text): return color(text, 40)
def bg_red(text): return color(text, 41)
def bg_green(text): return color(text, 42)
def bg_yellow(text): return color(text, 43)
def bg_blue(text): return color(text, 44)
def bg_magenta(text): return color(text, 45)
def bg_cyan(text): return color(text, 46)
def bg_white(text): return color(text, 47)


# # bright backgrounds (опционально)
# def bg_bright_black(text): return bg_color(text, 100)
# def bg_bright_red(text): return bg_color(text, 101)
# def bg_bright_green(text): return bg_color(text, 102)
# def bg_bright_yellow(text): return bg_color(text, 103)
# def bg_bright_blue(text): return bg_color(text, 104)
# def bg_bright_magenta(text): return bg_color(text, 105)
# def bg_bright_cyan(text): return bg_color(text, 106)
# def bg_bright_white(text): return bg_color(text, 107)