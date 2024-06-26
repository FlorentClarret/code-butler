from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import click
from rich.console import Console

from code_butler.__about__ import __version__
from code_butler.cli.application import Application
from code_butler.cli.config import config
from code_butler.cli.run import run

if TYPE_CHECKING:
    from typing import Optional


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
def code_butler(ctx: click.Context, config_file: Optional[str]) -> None:
    if config_file:
        path = Path(config_file)
        app = Application(ctx.exit, path)
        if not path.is_file():
            app.abort(f"The selected config file `{path}` does not exist.")
    else:
        app = Application(ctx.exit)
        if not app.config_file.path.is_file():
            try:
                app.config_file.restore()
            except OSError:  # no cov
                app.abort(
                    f"Unable to create config file located at `{app.config_file.path!s}`. Please check your permissions."
                )

    try:
        app.config_file.load()
    except OSError as e:  # no cov
        app.abort(f"Error loading configuration: {e}")

    # Store it so it can be used by sub-commands
    ctx.obj = app


code_butler.add_command(config)
code_butler.add_command(run)


def main() -> int:  # no cov
    try:
        return code_butler(prog_name="code_butler", windows_expand_args=False)  # type: ignore
    except Exception:
        console = Console()
        console.print_exception(suppress=[click])
        return 1
