import click

from code_butler.cli.config.edit import edit
from code_butler.cli.config.explore import explore
from code_butler.cli.config.find import find
from code_butler.cli.config.restore import restore
from code_butler.cli.config.set import set_value
from code_butler.cli.config.show import show


@click.group(short_help="Manage the config file")
def config():
    pass


config.add_command(edit)
config.add_command(explore)
config.add_command(find)
config.add_command(restore)
config.add_command(set_value)
config.add_command(show)
