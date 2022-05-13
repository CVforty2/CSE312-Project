#fills in an html template. Define varialbes to be enclosed by ${some_var}, and call the function with some_var=something
from util.debug.debug import debug_print


def template(filename: str = "", **kwargs) -> bytes:
    #read the html file
    html: str = open(filename, "r").read()
    for replacee, replacer in kwargs.items():
        html = html.replace(f"${{{replacee}}}", replacer)

    return html.encode()

