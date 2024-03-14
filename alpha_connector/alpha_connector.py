import logging
import os
from pathlib import Path

import dotenv
import numpy as np
import pandas as pd
import requests
import xarray as xr
import yaml

from .alpha_xarray import json_to_xarray, verify_json

dotenv.load_dotenv()

API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

# Load the config file
config_path = Path(__file__).parent / "config.yaml"
with open(config_path) as f:
    config = yaml.safe_load(f)

# log to txt file
logging.basicConfig(filename="plutus.log", level=logging.DEBUG)


class AlphaVantage:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://www.alphavantage.co/query?"

    def get_intraday(self, interval, symbol):
        function = config["core"]["intraday"]
        url = f"{self.base_url}function={function}&symbol={symbol}&interval={interval}&apikey={self.api_key}"
        logging.info(f"Requesting data from {url}")
        r = requests.get(url)
        data = r.json()

        # Verify the data
        verify_json(data)

        # Convert data to xarray
        ds = json_to_xarray(data, interval)

        return ds

    def get_daily(self, symbol):
        function = config["core"]["daily"]
        url = (
            f"{self.base_url}function={function}&symbol={symbol}&apikey={self.api_key}"
        )
        logging.info(f"Requesting data from {url}")
        r = requests.get(url)
        data = r.json()

        # Verify the data
        verify_json(data)

        # Convert data to xarray
        ds = json_to_xarray(data, "Daily")

        return ds

    def get_weekly(self, symbol):
        function = config["core"]["weekly"]
        url = (
            f"{self.base_url}function={function}&symbol={symbol}&apikey={self.api_key}"
        )
        logging.info(f"Requesting data from {url}")
        r = requests.get(url)
        data = r.json()

        # Verify the data
        verify_json(data)

        # Convert data to xarray
        ds = json_to_xarray(data, "Weekly")

        return ds

    def get_monthly(self, symbol):
        function = config["core"]["monthly"]
        url = (
            f"{self.base_url}function={function}&symbol={symbol}&apikey={self.api_key}"
        )
        logging.info(f"Requesting data from {url}")
        r = requests.get(url)
        data = r.json()

        # Verify the data
        verify_json(data)

        # Convert data to xarray
        ds = json_to_xarray(data, "Monthly")

        return ds


if __name__ == "__main__":
    api_key = API_KEY
    # print("Hello World!")
    av = AlphaVantage(api_key)
    print(av.base_url)
    data = av.get_intraday("1min", "IBM")

    attrs = data.attrs
    print(attrs)
