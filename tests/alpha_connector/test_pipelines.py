import logging
import os

import dotenv
import numpy as np
import pytest
import requests_mock
import xarray as xr

from alpha_connector.alpha_connector import FinancialModelingPrep

dotenv.load_dotenv()
FMP_API_KEY = os.getenv("FMP_API_KEY")


@pytest.fixture
def fmp():
    dotenv.load_dotenv()
    return FinancialModelingPrep(api_key=FMP_API_KEY)


def test_get_quote(fmp):
    response = fmp.get_quote("AAPL")
    assert "symbol" in response[0].keys()


def test_get_historical_price(fmp):
    response = fmp.get_historical_price("AAPL", "2024-01-01", "2024-02-02")
    assert isinstance(response, xr.Dataset)


def test_get_historical_chart(fmp):
    response = fmp.get_historical_chart("AAPL", "1min", "2021-01-01", "2021-01-02")
    assert isinstance(response, list)


def test_get_historical_chart_bad_time_delta(fmp):
    with pytest.raises(ValueError):
        fmp.get_historical_chart("AAPL", "1m", "2021-01-01", "2021-01-02")
