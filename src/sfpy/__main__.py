import code
import logging
import os
import pathlib
import sys
from typing import Iterable

import click
from click import BadArgumentUsage, BadOptionUsage, BadParameter
from click.exceptions import ClickException

from . import __version__

@click.command()
@click.version_option(__version__, package_name="aexpy", prog_name="aexpy", message="%(prog)s v%(version)s.")
def main() -> None:
    """
    scheme-from-python

    An experimental scheme interpreter in Python.

    Repository: https://github.com/StardustDL/scheme-from-python
    """


if __name__ == '__main__':
    main()
