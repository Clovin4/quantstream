"""main module for the alpha_connector package"""

from typing import Optional

import xarray as xr

from .fmp_connector import FinancialModelingPrep


def get_timeseries(
    symbols: list[str] | str,
    from_date: str,
    to_date: str,
    connector: FinancialModelingPrep,
    time_delta: Optional[str] = "5min",
    output_format: Optional[str] = "xarray",
) -> xr.Dataset:
    """Get timeseries data for a list of symbols."""
    if not isinstance(symbols, list):
        symbols = [symbols]

    if output_format not in ["xarray"]:
        raise ValueError("output_format must be 'xarray' or 'pandas'")

    for symbol in symbols:
        if not isinstance(symbol, str):
            raise ValueError("symbols must be a list of strings")

    if output_format == "xarray":
        dataset = xr.Dataset()
        for symbol in symbols:
            temp = connector.get_intraday(symbol, time_delta, from_date, to_date)
            # extract the data from the xarray dataset
            open_vals = xr.DataArray(
                temp["open"].values,
                dims=["time"],
            )
            low = xr.DataArray(
                temp["low"].values,
                dims=["time"],
            )
            high = xr.DataArray(
                temp["high"].values,
                dims=["time"],
            )
            close = xr.DataArray(
                temp["close"].values,
                dims=["time"],
            )
            volume = xr.DataArray(
                temp["volume"].values,
                dims=["time"],
            )

            # create a new dataset with the extracted data
            dataset[f"{symbol.lower()}_open"] = open_vals
            dataset[f"{symbol.lower()}_low"] = low
            dataset[f"{symbol.lower()}_high"] = high
            dataset[f"{symbol.lower()}_close"] = close
            dataset[f"{symbol.lower()}_volume"] = volume

            dataset.coords["time"] = temp["time"]

        dataset.attrs["time_delta"] = time_delta
        dataset.attrs["from_date"] = from_date
        dataset.attrs["to_date"] = to_date

        return dataset
