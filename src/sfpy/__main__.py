import code
from email.policy import default
from importlib.resources import read_text
import logging
import os
from pathlib import Path
import sys
from typing import Iterable

import click
from click import BadArgumentUsage, BadOptionUsage, BadParameter
from click.exceptions import ClickException

from . import __version__


@click.command()
@click.version_option(__version__, package_name="scheme-from-python", prog_name="aexpy", message="%(prog)s v%(version)s.")
@click.option('-f', '--file', type=click.Path(exists=True, file_okay=True, dir_okay=False, resolve_path=True, path_type=Path), default=None, help="Source file to evaluate.")
@click.option('-e', '--expr', default=None, help="Expression to evaluate.")
def main(expr: str | None = None, file: Path | None = None) -> None:
    """
    scheme-from-python

    An experimental scheme interpreter in Python.

    Repository: https://github.com/StardustDL/scheme-from-python
    """

    from .interpreters import Interpreter
    interpreter = Interpreter()

    if expr:
        print(interpreter.interprete(expr))
    elif file:
        print(interpreter.interprete(file.read_text()))
    else:
        interpreter.interact()


if __name__ == '__main__':
    main()
