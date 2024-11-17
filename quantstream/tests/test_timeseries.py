from quantstream.modules.timeseries import get_quote, get_intraday, get_daily
from quantstream.datasets.findataset import FinDataset
from quantstream.config import set_fmp_api_key
import pytest
import datetime

today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)

@pytest.fixture
def set_api_key():
    from quantstream.config import set_fmp_api_key
    set_fmp_api_key("test_key")

def test_get_quote():
    data = get_quote("AAPL")
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["symbol"] == "AAPL"


def test_get_intraday():
    data = get_intraday("AAPL", "5min", yesterday, today)
    assert isinstance(data, FinDataset)
    assert len(data) > 0

def test_get_daily():
    data = get_daily("AAPL", yesterday, today)
    assert isinstance(data, FinDataset)
    assert len(data) > 0
