from typing import Optional

import logging
import os
from pathlib import Path

import dotenv
import numpy as np
import pandas as pd
import requests
import xarray as xr
import yaml

from .data_modeling import FinDataset
from .technicals import daily, intraday, quote

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

    def get_daily(self, symbol, from_date=None, to_date=None) -> FinDataset:
        response = daily(self.api_key, symbol, from_date, to_date)
        return FinDataset.from_json(response)

    def get_intraday(
        self, symbol, time_delta, from_date, to_date, time_series=None
    ) -> FinDataset:
        response = intraday(
            self.api_key, symbol, time_delta, from_date, to_date, time_series
        )
        ds = FinDataset.from_json(response)
        ds.attrs["time_delta"] = time_delta
        ds.attrs["from_date"] = from_date
        ds.attrs["to_date"] = to_date

        return ds
