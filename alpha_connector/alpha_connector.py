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
logging.basicConfig(filename="connector.log", level=logging.DEBUG)


class AlphaVantage:
    def __init__(self, api_key: str = None):
        if api_key is None:
            api_key = os.getenv("ALPHAVANTAGE_API_KEY")
        if not api_key or not isinstance(api_key, str):
            raise ValueError(
                "The AlphaVantage API key must be provided "
                "either through the key parameter or "
                "through the environment variable "
                "ALPHAVANTAGE_API_KEY. Get a free key "
                "from the alphavantage website: "
                "https://www.alphavantage.co/support/#api-key"
            )
        self.api_key = api_key
        self.base_url = "https://www.alphavantage.co/query?"

    def get_intraday(
        self,
        symbol,
        interval="5min",
        adjusted=True,
        extended_hours=False,
        month=None,
        outputsize="compact",
        datatype="json",
    ):
        function = config["core"]["intraday"]
        params = {
            "function": function,
            "symbol": symbol,
            "interval": interval,
            "apikey": self.api_key,
            "outputsize": outputsize,
            "datatype": datatype,
        }

        logging.info("Requesting data for symbol: %s, interval: %s", symbol, interval)

        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)

            data = response.json()

            # Verify the data. Assuming verify_json throws an exception on failure
            verify_json(data)

            # Convert data to xarray. Assuming json_to_xarray throws an exception on failure
            ds = json_to_xarray(data, interval)

            return ds

        except requests.exceptions.HTTPError as http_err:
            logging.error(f"HTTP error occurred: {http_err}")  # Python 3.6+
            # Handle specific HTTP errors if needed
        except requests.exceptions.RequestException as err:
            logging.error(f"Error occurred during request to Alpha Vantage: {err}")
        except ValueError as ve:
            logging.error(f"Error processing JSON data: {ve}")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")

        # Return None or raise an exception if errors should propagate up
        return None

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
