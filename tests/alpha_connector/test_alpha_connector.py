import logging
import os

import dotenv
import pytest

from alpha_connector.alpha_connector import AlphaVantage
from alpha_connector.alpha_xarray import verify_json

dotenv.load_dotenv()
API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")

logging.basicConfig(filename="connector.log", level=logging.DEBUG)


@pytest.fixture
def av():
    return AlphaVantage(API_KEY)


def test_verify_json():
    """Test the verify_json function."""
    data = {
        "Error Message": "Invalid API call. Please retry or visit the documentation (https://www.alphavantage.co/documentation/) for TIME_SERIES_INTRADAY."
    }
    with pytest.raises(ValueError):
        verify_json(data)

    data = {"Information": "Please consider optimizing your API call frequency."}
    with pytest.raises(ValueError):
        verify_json(data)

    data = {
        "Note": "Thank you for using Alpha Vantage! Our standard API call frequency is 5 calls per minute and 500 calls per day. Please visit https://www.alphavantage.co/premium/ if you would like to target a higher API call frequency."
    }
    with pytest.raises(ValueError):
        verify_json(data)

    data = {
        "Meta Data": {
            "1. Information": "Intraday (5min) open, high, low, close prices and volume",
            "2. Symbol": "AAPL",
            "3. Last Refreshed": "2021-08-27 20:00:00",
            "4. Interval": "5min",
            "5. Output Size": "Compact",
            "6. Time Zone": "US/Eastern",
        },
        "Time Series (5min)": {
            "2021-08-27 20:00:00": {
                "1. open": "148.3000",
                "2. high": "148.3000",
                "3. low": "148.3000",
                "4. close": "148.3000",
                "5. volume": "100",
            }
        },
    }
    assert verify_json(data)


def test_init(av):
    """Test the __init__ method."""
    assert av.api_key == API_KEY
    assert av.base_url == "https://www.alphavantage.co/query?"


params = [
    ("AAPL", "5min"),
    ("GOOGL", "15min"),
    ("MSFT", "30min"),
    ("TSLA", "60min"),
]


@pytest.mark.parametrize("symbol, interval", params)
def test_get_intraday(av, symbol, interval):
    """Test the get_intraday method."""
    data = av.get_intraday(symbol, interval)
    if isinstance(data, str):
        assert (
            data
            == "Thank you for using Alpha Vantage! Our standard API rate limit is 25 requests per day. Please subscribe to any of the premium plans at https://www.alphavantage.co/premium/ to instantly remove all daily rate limits."
        )
    else:
        assert (
            data.attrs["1. Information"]
            == f"Intraday ({interval}) open, high, low, close prices and volume"
        )
        assert data.attrs["2. Symbol"] == symbol
        assert data.attrs["3. Last Refreshed"] is not None
        assert data.attrs["4. Interval"] == interval
        assert data.attrs["5. Output Size"] == "Compact"
        assert data.attrs["6. Time Zone"] == "US/Eastern"


"""
TODO: Add tests for the following methods:
- get_daily
- get_weekly
- get_monthly
"""
