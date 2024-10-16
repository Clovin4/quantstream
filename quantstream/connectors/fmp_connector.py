from typing import Optional
from datetime import date
import logging
import os


from .findataset import FinDataset
from .timeseries import daily, intraday, quote
from .fundamentals import (
    company_profile,
    stock_list,
    etf_list,
    income_statement,
    balance_sheet_statement,
    cash_flow_statement,
)

# log to txt file
logging.basicConfig(filename="connector.log", level=logging.DEBUG)


class FmpConnector:
    """_summary_"""

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

    def list_symbols(self) -> dict:
        """https://financialmodelingprep.com/api/v3/stock/list"""
        return stock_list(self.api_key)

    def list_etfs(self) -> dict:
        """https://financialmodelingprep.com/api/v3/etf/list"""
        return etf_list(self.api_key)

    def get_quote(self, symbol) -> dict:
        """_summary_

        Args:
            symbol (_type_): _description_

        Returns:
            _type_: _description_
        """
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
        """Get intraday financial data for a given symbol.

        Args:
            symbol (str): The symbol of the financial instrument.
            time_delta (str): The time interval for the data (e.g., '1min', '5min', '15min', '30min', '60min').
            from_date (str): The start date of the data in the format 'YYYY-MM-DD'.
            to_date (str): The end date of the data in the format 'YYYY-MM-DD'.
            time_series (str, optional): The type of time series data to retrieve (e.g., 'open', 'high', 'low', 'close', 'volume'). Defaults to None.

        Returns:
            FinDataset: A dataset containing the intraday financial data.
        """
        response = intraday(
            self.api_key, symbol, time_delta, from_date, to_date, time_series
        )
        ds = FinDataset.from_json(response)
        ds.attrs["time_delta"] = time_delta
        ds.attrs["from_date"] = from_date
        ds.attrs["to_date"] = to_date

        return ds

    def get_company_profile(self, symbol):
        try:
            response = company_profile(self.api_key, symbol)
            if isinstance(response, list):
                return response[0]
            return response
        except Exception as e:
            logging.error(f"Error fetching company profile for {symbol}: {str(e)}")
            raise

    def get_income_statement(self, symbol: str, period: str = "annual"):
        """https://site.financialmodelingprep.com/developer/docs#income-statements-financial-statements

        Args:
            symbol (_type_): _description_
            period (_type_): _description_
        """
        return income_statement(self.api_key, symbol, period)

    def get_balance_sheet(self, symbol: str, period: str = "annual"):
        """_summary_

        Args:
            symbol (_type_): _description_
            period (_type_): _description_
        """
        return balance_sheet_statement(self.api_key, symbol, period)

    def get_cash_flow(self, symbol: str, period: str = "annual"):
        """_summary_

        Args:
            symbol (_type_): _description_
            period (_type_): _description_
        """
        return cash_flow_statement(self.api_key, symbol, period)
