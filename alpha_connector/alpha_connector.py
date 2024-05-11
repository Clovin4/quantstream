import logging
import os
from pathlib import Path

import dotenv
import numpy as np
import pandas as pd
import requests
import xarray as xr
import yaml

from .data_modeling import json_to_xarray
from .technicals import historical_chart, historical_price_full, quote

# Load the config file
config_path = Path(__file__).parent / "av_config.yaml"
with open(config_path) as f:
    config = yaml.safe_load(f)

# log to txt file
logging.basicConfig(filename="connector.log", level=logging.DEBUG)


class FinancialModelingPrep:
    def __init__(self, api_key: str = None):
        if api_key is None:
            logging.info("API key not provided. Checking environment variable.")
            api_key = os.getenv("FMP_API_KEY")
            logging.info(f"API key found: {api_key}")

        if not api_key or not isinstance(api_key, str):
            raise ValueError(
                "The FMP API key must be provided "
                "either through the key parameter or "
                "through the environment variable "
                "FMP_API_KEY. Get a free key "
                "from the financialmodelingprep website: "
                "https://financialmodelingprep.com/developer/docs/"
            )
        self.api_key = api_key

    def get_quote(self, symbol):
        response = quote(self.api_key, symbol)
        return response

    def get_historical_price(self, symbol, from_date=None, to_date=None):
        response = historical_price_full(self.api_key, symbol, from_date, to_date)
        return json_to_xarray(response)

    def get_historical_chart(
        self, symbol, time_delta, from_date, to_date, time_series=None
    ):
        response = historical_chart(
            self.api_key, symbol, time_delta, from_date, to_date, time_series
        )
        return response
