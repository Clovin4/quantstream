from typing import Optional
from datetime import date
import logging
import os


from .data_modeling import FinDataset
from .timeseries import daily, intraday, quote

# log to txt file
logging.basicConfig(filename="connector.log", level=logging.DEBUG)


class FinancialModelingPrep:
    def __init__(self, api_key: str = None):
        if not api_key or not isinstance(api_key, str):
            api_key = os.getenv("FMP_API_KEY")
            if not api_key:
                raise ValueError(
                    "The FMP API key must be provided "
                    "either through the key parameter or "
                    "through the environment variable "
                    "FMP_API_KEY. Get a free key "
                    "from the financialmodelingprep website: "
                    "https://financialmodelingprep.com/developer/docs/"
                )
            logging.info("FMP API key loaded from environment variable.")
        self.api_key = api_key

    def get_quote(self, symbol):
        response = quote(self.api_key, symbol)
        return response

    def get_daily(
        self,
        symbol: str,
        from_date: Optional[date] = None,
        to_date: Optional[date] = None,
    ) -> FinDataset:
        """
        Fetch daily financial data for a given symbol.

        Args:
            symbol (str): The stock symbol to fetch data for.
            from_date (date, optional): Start date for the data range.
            to_date (date, optional): End date for the data range.

        Returns:
            FinDataset: A dataset containing the daily financial data.

        Raises:
            ValueError: If the symbol is invalid or dates are in incorrect format.
        """
        if not symbol or not isinstance(symbol, str):
            raise ValueError("Invalid symbol provided")

        try:
            logging.info(f"Fetching daily data for {symbol}")
            response = daily(self.api_key, symbol, from_date, to_date)
            return FinDataset.from_json(response)
        except Exception as e:
            logging.error(f"Error fetching daily data for {symbol}: {str(e)}")
            raise

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
