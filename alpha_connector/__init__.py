# type: ignore[attr-defined]
"""Awesome `alpha_connector` is a Python cli/package created with https://github.com/TezRomacH/python-package-template"""

from importlib import metadata as importlib_metadata

from .connectors.fmp_connector import FinancialModelingPrep
from .core.portfolio import Portfolio


def get_version() -> str:
    try:
        return importlib_metadata.version(__name__)
    except importlib_metadata.PackageNotFoundError:  # pragma: no cover
        return "unknown"


version: str = get_version()

__all__ = ["FinancialModelingPrep", "Portfolio", "version"]
