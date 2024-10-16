# type: ignore[attr-defined]
"""QuantStream: A Python library for financial data analysis and portfolio management."""

from importlib import metadata as importlib_metadata

from .connectors.fmp_connector import FmpConnector
from .groups.portfolio import Portfolio

# import all functions from financial_timeseries.returns
from .financial_timeseries.returns import absolute_returns, percentage_returns, log_returns, rolling_statistics


def get_version() -> str:
    try:
        return importlib_metadata.version(__name__)
    except importlib_metadata.PackageNotFoundError:  # pragma: no cover
        return "unknown"


version: str = get_version()

__all__ = ["FmpConnector", "Portfolio", "version"]
__all__ += ["absolute_returns", "percentage_returns", "log_returns", "rolling_statistics"]
