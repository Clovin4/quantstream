import os

import dotenv
import pytest
import xarray as xr

from quantstream.connectors.data_modeling import FinDataset
from quantstream.connectors.fmp_connector import FinancialModelingPrep

# dotenv.load_dotenv()
FMP_API_KEY = os.getenv("FMP_API_KEY")


@pytest.fixture
def fmp():
    # at some point we'll need to use a secrets manager
    dotenv.load_dotenv()
    return FinancialModelingPrep(api_key=FMP_API_KEY)


#################### unit tests ####################
# region unit tests


def test_get_quote(fmp):
    response = fmp.get_quote("AAPL")
    assert "symbol" in response[0].keys()


def test_get_daily(fmp):
    response = fmp.get_daily("AAPL", "2024-01-01", "2024-02-02")
    assert isinstance(response, xr.Dataset)


def test_get_intraday(fmp):
    response = fmp.get_intraday("AAPL", "1hour", "2024-01-01", "2024-02-02")
    assert isinstance(response, FinDataset)


def test_get_intraday_bad_time_delta(fmp):
    with pytest.raises(ValueError):
        fmp.get_intraday("AAPL", "1m", "2021-01-01", "2021-01-02")


#################### integration tests ####################
# region integration tests
