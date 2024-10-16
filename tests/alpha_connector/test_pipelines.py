import os

import pytest
import xarray as xr

from quantstream.connectors.findataset import FinDataset
from quantstream.connectors.fmp_connector import FmpConnector

FMP_API_KEY = os.getenv("FMP_API_KEY")


@pytest.fixture
def fmp():
    # at some point we'll need to use a secrets manager
    return FmpConnector(api_key=FMP_API_KEY)


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

def test_get_company_profile(fmp):
    response = fmp.get_company_profile("AAPL")
    assert "symbol" in response.keys()

def test_get_income_statement(fmp):
    response = fmp.get_income_statement("AAPL")
    assert isinstance(response, list)

def test_get_balance_sheet_statement(fmp):
    response = fmp.get_balance_sheet("AAPL")
    assert isinstance(response, list)

def test_get_cash_flow_statement(fmp):
    response = fmp.get_cash_flow("AAPL")
    assert isinstance(response, list)

def test_list_symbols(fmp):
    response = fmp.list_symbols()
    assert isinstance(response, list)

def test_list_etfs(fmp):
    response = fmp.list_etfs()
    assert isinstance(response, list)


#################### integration tests ####################
# region integration tests
