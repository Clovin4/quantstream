import os

import dotenv
import pytest

dotenv.load_dotenv()

API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

from alpha_connector.alpha_connector import AlphaVantage


@pytest.mark.parametrize(
    ("interval", "symbol"),
    [
        ("5min", "IBM"),
        ("1min", "AAPL"),
        ("15min", "GOOGL"),
    ],
)
def test_get_data(interval, symbol):
    """Test get_data method."""
    av = AlphaVantage(API_KEY)
    data = av.get_intraday(interval, symbol)
    assert data is not None
