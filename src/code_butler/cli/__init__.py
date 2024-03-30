from pathlib import Path

import click

from code_butler.__about__ import __version__
from rich.console import Console

from code_butler.cli.application import Application
from code_butler.cli.config import config
from code_butler.cli.run import run


@click.group(
    context_settings={"help_option_names": ["-h", "--help"]},
    invoke_without_command=True,
)
@click.option(
    "--config",
    "-c",
    "config_file",
    envvar="CODE_BUTLER_CONFIG",
    help="The path to a custom config file to use.",
)
@click.version_option(version=__version__, prog_name="Code Butler")
@click.pass_context
def code_butler(ctx, config_file):
    if config_file:
        path = Path(config_file)
        app = Application(path)
        if not path.is_file():
            print(f"The selected config file `{path}` does not exist.")
            ctx.exit(1)
    else:
        app = Application()
        if not app.config_file.path.is_file():
            try:
                app.config_file.restore()
            except OSError:  # no cov
                print(
                    f"Unable to create config file located at `{str(app.config_file.path)}`. Please check your permissions."
                )
                ctx.exit(1)

    try:
        app.config_file.load()
    except OSError as e:  # no cov
        print(f"Error loading configuration: {e}")
        ctx.exit(1)

    # Store it so it can be used by sub-commands
    ctx.obj = app


code_butler.add_command(config)
code_butler.add_command(run)


def main():  # no cov
    try:
        return code_butler(prog_name="code_butler", windows_expand_args=False)
    except Exception:
        console = Console()
        console.print_exception(suppress=[click])
        return 1
