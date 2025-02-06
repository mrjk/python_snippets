#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Version: 08-2024

"""MyApp CLI interface

This CLI provides a similar experience as the git CLI, but in Python with Typer.

Example:
``` py title="test.py"
from my_app.cli import cli_app

myapp = cli_app()
myapp.info()
myapp.apply()
```

This is a quite complete CLI template for your App, you will probably want
to remove 80% of this file.

To start, you need to replace the following strings:
* `MyApp`
* `myapp`

When used with poetry:
```
[tool.poetry.scripts]
my_app = "my_app.cli:cli_run"
```

Author: MrJK
License: GPLv3
"""

import logging
import os
import sys
import traceback
from enum import Enum
from pathlib import Path
from pprint import pprint
from typing import Optional

import typer

# import sh
# import pyaml
# from loguru import logger

# Base Application example
# ===============================

logging.basicConfig(format="%(levelname)8s: %(message)s")
logger = logging.getLogger()


# Application Application
# ===============================

# logger = logging.getLogger(name="myapp.cli")

# Import from: app.py
# from app import MyApp, MyAppException, OutputFormat, app_version
# Or:
app_version = "0.1.0"

class MyAppException(Exception):
    """Generic MyApp exception"""
    rc = 1

class MyApp:
    "This is MyApp Class"

    version = app_version
    name = "My Super App"

    def __init__(self, path):
        self.path = path

    def hello(self):
        "Simple Hello World"
        print(f"Hello World: {self.path}")

    def world(self):
        "Print three time World"
        print("Hello World World World")
    
    def fail(self):
        "Return an application exception"
        raise MyAppException("This failure does not create python tracebacks")

        
class OutputFormat(str, Enum):
    "Available output formats"

    # pylint: disable=invalid-name
    yaml = "yaml"
    json = "json"
    toml = "toml"


# Core application definition
# ===============================

# Define Typer application
# -------------------
cli_app = typer.Typer(
    help="MyApp, that does something",
    invoke_without_command=True,
    no_args_is_help=True,
)


# Define an init function, with common options
# -------------------
@cli_app.callback()
def main(
    ctx: typer.Context,
    verbose: int = typer.Option(0, "--verbose", "-v", count=True, min=0, max=3, help="Increase verbosity"),
    working_dir: Path = typer.Option(
        ".",  # For relative paths
        # os.getcwd(),  # For abolute Paths
        "-c",
        "--config",
        help="Path of myapp.yml configuration file or directory.",
        envvar="MYAPP_PROJECT_DIR",
    ),
    version: bool = typer.Option(
        False,
        "--version",
        "-V",
        help="Show version",
    ),
):
    """
    MyApp Command Line Interface.
    """

    # Set logging level
    # -------------------
    # 50: Crit
    # 40: Err
    # 30: Warn
    # 20: Info
    # 10: Debug
    # 0: Not set
    logger = logging.getLogger(None if verbose >= 3 else __package__)
    verbose = 30 - (verbose * 10)
    verbose = verbose if verbose > 10 else logging.DEBUG
    logger.setLevel(level=verbose)

    # Init myapp
    # -------------------
    if version:
        print(app_version)
        return

    ctx.obj = {
        "myapp": MyApp(working_dir),
    }


# Simple commands example
# ===============================


@cli_app.command("help")
def cli_help(
    ctx: typer.Context,
):
    """Show this help message"""
    print(ctx.parent.get_help())


@cli_app.command("logging")
def cli_logging():
    """Test logging"""

    # Test logging:
    # -------------------
    logger.critical("SHOW CRITICAL")
    logger.error("SHOW ERROR")
    logger.warning("SHOW WARNING")
    logger.info("SHOW INFO")


# pylint: disable=redefined-builtin
@cli_app.command("command1")
def cli_command1(
    ctx: typer.Context,
    mode: Optional[str] = typer.Option(
        "Default Mode",
        help="Write anything here",
    ),
    format: OutputFormat = typer.Option(
        OutputFormat.yaml.value,
        help="Output format",
    ),
    target: Optional[str] = typer.Argument(
        None,
        help="Target directory or all",
    ),
):
    """Command1 example"""
    myapp = ctx.obj["myapp"]

    print(
        f"Run {myapp} with '{target}' as target in mode '{mode}' in format '{format}'"
    )
    print("This is a dump of our cli context:")
    pprint(ctx.__dict__)

    print("Run MyApp")
    myapp.hello()
    myapp.world()


# Source Command SubGroup Example
# ===============================
cli_src = typer.Typer(help="Manage sources")
cli_app.add_typer(cli_src, name="group1")


@cli_src.callback()
def src_callback():
    """
    Manage sources in the app.
    """
    print("Executed before all source commands")


@cli_src.command("ls")
def src_ls():
    """List sources"""
    print("List sources")


@cli_src.command("install")
def src_install():
    """Install sources"""
    print("Install a source")


@cli_src.command("update")
def src_update():
    """Update sources"""
    print("Update sources")


# Exception handler
# ===============================
def clean_terminate(err):
    "Terminate nicely the program depending the exception"

    user_errors = (
        PermissionError,
        FileExistsError,
        FileNotFoundError,
        InterruptedError,
        IsADirectoryError,
        NotADirectoryError,
        TimeoutError,
    ) + (
        MyAppException,
        # yaml.parser.ParserError,
        # sh.ErrorReturnCode,
    )

    if isinstance(err, user_errors):

        # Fetch extra error informations
        rc = int(getattr(err, "rc", getattr(err, "errno", 1)))
        advice = getattr(err, "advice", None)
        if advice:
            logger.warning(advice)

        # Log error and exit
        logger.error(err)
        err_name = err.__class__.__name__
        logger.critical("MyApp exited with error %s (%s)", err_name, rc)
        sys.exit(rc)

    # Developper bug catchall
    rc = 255
    logger.error(traceback.format_exc())
    logger.critical("Uncatched error: %s", err.__class__)
    logger.critical("This is a bug, please report it.")
    sys.exit(rc)

# Core application definition
# ===============================


def cli_run():
    "Return a MyApp App instance"
    try:
        return cli_app()
    # pylint: disable=broad-except
    except Exception as err:
        clean_terminate(err)

if __name__ == "__main__":
    cli_run()
