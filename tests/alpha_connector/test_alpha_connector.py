import os

import dotenv
import pytest

dotenv.load_dotenv()

API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

from alpha_connector.alpha_connector import AlphaVantage


@pytest.mark.parametrize(
    ("function", "interval", "symbol"),
    [
        ("TIME_SERIES_INTRADAY", "5min", "IBM"),
        ("TIME_SERIES_INTRADAY", "1min", "AAPL"),
        ("TIME_SERIES_INTRADAY", "15min", "GOOGL"),
    ],
)
def test_get_data(function, interval, symbol):
    """Test get_data method."""
    av = AlphaVantage(API_KEY)
    data = av.get_intraday(function, interval, symbol)
    assert data is not None
