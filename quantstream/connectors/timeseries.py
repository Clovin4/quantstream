import typing

from .url_methods import __return_json_v3, __validate_time_delta
from .urls import FMP_URLS

fmp = FMP_URLS()


def quote(
    apikey: str, symbol: typing.Union[str, list[str]]
) -> typing.Optional[list[dict]]:
    """Retrieve quote information for a given symbol or list of symbols.

    Args:
        apikey (str): The API key for accessing the quote information.
        symbol (typing.Union[str, typing.List[str]]): The symbol or list of symbols for which to retrieve quote information.

    Returns:
        typing.Optional[typing.List[typing.Dict]]: A list of dictionaries containing the quote information for the given symbol(s).
            Each dictionary represents a quote and contains various fields such as symbol, price, volume, etc.
            Returns None if no quote information is available.
    """
    if isinstance(symbol, list):
        symbol = ",".join(symbol)
    path = f"quote/{symbol}"
    query_vars = {"apikey": apikey}
    return __return_json_v3(path=path, params=query_vars)


def intraday(
    apikey: str,
    symbol: str,
    time_delta: str,
    from_date: str,
    to_date: str,
    time_series: str = fmp.default_line_param,
) -> typing.Optional[list[dict]]:
    """Fetches intraday historical chart data for a given symbol.

    Args:
        apikey (str): The API key for accessing the data.
        symbol (str): The symbol for the stock or security.
        time_delta (str): The time interval for the data (e.g., '1min', '5min', '15min', '30min', '1hour').
        from_date (str): The starting date for the data in the format 'YYYY-MM-DD'.
        to_date (str): The ending date for the data in the format 'YYYY-MM-DD'.
        time_series (str, optional): The type of time series data to fetch. Defaults to fmp.default_line_param.

    Returns:
        typing.Optional[typing.List[typing.Dict]]: A list of dictionaries representing the intraday historical chart data.
    """
    path = f"historical-chart/{__validate_time_delta(time_delta)}/{symbol}"
    query_vars = {"apikey": apikey}
    query_vars = {
        "apikey": apikey,
    }
    if time_series:
        query_vars["timeseries"] = time_series
    if from_date:
        query_vars["from"] = from_date
    if to_date:
        query_vars["to"] = to_date
    return __return_json_v3(path=path, params=query_vars)


def daily(
    apikey: str,
    symbol: typing.Union[str, list],
    from_date: str = None,
    to_date: str = None,
) -> typing.Optional[list[dict]]:
    """Fetches daily historical stock prices for the specified symbol(s).

    Args:
        apikey (str): The API key for accessing the stock price data.
        symbol (typing.Union[str, typing.List]): The symbol(s) of the stock(s) to fetch data for.
            It can be a single symbol or a list of symbols.
        from_date (str, optional): The starting date for the historical data.
            If not provided, it fetches data from the earliest available date.
        to_date (str, optional): The ending date for the historical data.
            If not provided, it fetches data up to the latest available date.

    Returns:
        typing.Optional[typing.List[typing.Dict]]: A list of dictionaries containing the historical stock prices.
            Each dictionary represents a single day's data and includes information such as the date, open price,
            high price, low price, close price, volume, and adjusted close price.

    Raises:
        ValueError: If the API response indicates an error or an invalid request.

    """
    if isinstance(symbol, list):
        symbol = ",".join(symbol)
    path = f"historical-price-full/{symbol}"
    query_vars = {
        "apikey": apikey,
    }

    if from_date:
        query_vars["from"] = from_date
    if to_date:
        query_vars["to"] = to_date

    res = __return_json_v3(path=path, params=query_vars)

    if res.get("historicalStockList", res.get("historical", None)) is None:
        if res.get("Error Message"):
            raise ValueError(res["Error Message"])
        else:
            raise ValueError("Invalid request.")
    else:
        return_value = res.get("historicalStockList", res.get("historical", None))
        sorted_res = sorted(
            list(return_value),
            key=lambda x: x["date"],
        )
        return sorted_res
