# type: ignore[attr-defined]
from typing import Optional

from enum import Enum
from random import choice

import typer
from rich.console import Console

from alpha_connector import version
from alpha_connector.alpha_connector import AlphaVantage

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


@app.command(name="")
def main(
    symbol: str = typer.Option(
        ..., "-s", "--symbol", help="Ticker for asset analysis."
    ),
    function: str = typer.Option("Intraday", help="Interval for data."),
    interval: str = typer.Option("5min", help="Interval for data."),
    # start_date: str = typer.Option("2021-01-01", help="Start date for analysis."),
    # end_date: str = typer.Option("2021-12-31", help="End date for analysis."),
    api_key: str = typer.Option(
        ..., "-k", "--api-key", help="API key for Alpha Vantage."
    ),
    print_version: bool = typer.Option(
        None,
        "-v",
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Prints the version of the alpha_connector package.",
    ),
) -> None:
    """Print a greeting with a giving name."""

    if function == "Intraday":
        data = AlphaVantage(api_key).get_intraday(interval, symbol)
    elif function == "Daily":
        data = AlphaVantage(api_key).get_daily(interval, symbol)
    elif function == "Weekly":
        data = AlphaVantage(api_key).get_weekly(interval, symbol)
    elif function == "Monthly":
        data = AlphaVantage(api_key).get_monthly(interval, symbol)
    else:
        raise ValueError(f"Function {function} not recognized.")

    console.print(data)


if __name__ == "__main__":
    app()
