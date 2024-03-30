from rich.console import Console as RichConsole


class Console:
    def __init__(self, color: bool = True):
        self.__console = RichConsole(
            no_color=not color,
            markup=False,
            emoji=False,
            highlight=False,
        )

    def print(self, *args, **kwargs):
        self.__console.print(*args, **kwargs)
