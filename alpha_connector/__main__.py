from typing import Optional

import os
from enum import Enum
from random import choice

import typer
from rich.console import Console

from alpha_connector import version
from alpha_connector.fmp_connector import FinancialModelingPrep

app = typer.Typer(
    name="alpha_connector",
    help="Awesome `alpha_connector` is a Python cli/package created with https://github.com/TezRomacH/python-package-template",
    add_completion=False,
)
console = Console()


def version_callback(print_version: bool) -> None:
    """Print the version of the package."""
    if print_version:
        console.print(f"[yellow]alpha_connector[/] version: [bold blue]{version}[/]")
        raise typer.Exit()


def confirm_api_keys_callback(show_api_keys: bool) -> None:
    """Print the api keys."""
    if show_api_keys:
        console.print(f"[yellow]alpha_connector[/] version: [bold blue]{version}[/]")
        # look for keys in environment variables
        fmp_api_key = os.getenv("FMP_API_KEY")
        console.print(f"[yellow]FMP_API_KEY[/]: [bold blue]{fmp_api_key}[/]")
        av_api_key = os.getenv("ALPHAVANTAGE_API_KEY")
        console.print(f"[yellow]ALPHAVANTAGE_API_KEY[/]: [bold blue]{av_api_key}[/]")
        raise typer.Exit()


# TODO: rethink the command structure. Is the best use of this a cli that returns data or a package that returns data?
# Could the cli be more usefull as a data pipeline tool? A machine learning feature engineering tool? Or a data
# visualization tool?


@app.command(name="")
def main(
    print_version: bool = typer.Option(
        None,
        "-v",
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Prints the version of the alpha_connector package.",
    ),
    show_api_keys: bool = typer.Option(
        None,
        "-k",
        "--keys",
        callback=confirm_api_keys_callback,
        is_eager=True,
        help="Prints the api keys.",
    ),
) -> None:
    """Main entry point for the alpha_connector package."""
    console.print(
        "Welcome to the alpha_connector package. Use the --help flag to see available commands."
    )


if __name__ == "__main__":
    app()
