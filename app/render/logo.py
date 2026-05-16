from app.backend.colors import red, green, blue, magenta
from app.render.helpers import center_visible

def render_letters(*l: str) -> str:
    result = ""
    for i, let in enumerate(l):
        if i % 4 == 0:
            result += red(let)
        if i % 4 == 1:
            result += green(let)
        if i % 4 == 2:
            result += blue(let)
        if i % 4 == 3:
            result += magenta(let)
    return result


def render_logo(width: int):
    logo = f"""
    
    
                 (       *     (    (         )      )        
  *   )      )\\ )  (  `    )\\ ) )\\ )   ( /(   ( /(        
` )  /( (   (()/(  )\\))(  (()/((()/(   )\\())  )\\())   (   
 ( )(_)))\\   /(_))((_)()\\  /(_))/(_)) ((_)\\ |((_)\\    )\\  
(_(_())((_) (_))  (_()((_)(_)) (_))_    ((_)|_ ((_)_ ((_) 
{render_letters('|_   _|', '| __|', '| _ \\', ' |  \\/  |', '|_ _| ', '|   \\', '  / _ \\', '| |/ /', '| | | | ')}
{render_letters('  | |  ', '| _| ', '|   / ', '| |\\/| |', ' | |  ', '| |) |', '| (_) ', '| \' < ', '| |_| | ')}
{render_letters('  |_|  ', '|___|', '|_|_\\', ' |_|  |_|', '|___| ', '|___/  ', '\\___', '/ _|\\_\\', ' \\___/  ')}
"""

    lines = logo.strip("\n").splitlines()

    centered = "\n".join(
        center_visible(line, width)
        for line in lines
    )

    return centered

# \[([_ |\\/]+)\]