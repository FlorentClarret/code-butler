from __future__ import annotations

from typing import TYPE_CHECKING

import click

if TYPE_CHECKING:
    from code_butler.cli.application import Application


@click.command("set", short_help="Assign values to config file entries")
@click.argument("key")
@click.argument("value")
@click.pass_obj
def set_value(app: Application, key: str, value: str) -> None:
    app.config_file.config.set_field(key, value)
    app.config_file.save()
