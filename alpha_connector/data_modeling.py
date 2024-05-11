import typing

import json

import numpy as np
import pandas as pd
import xarray as xr


def json_to_xarray(data: list[dict]) -> xr.Dataset:
    """Convert json data to xarray."""
    pd_data = pd.DataFrame(data)

    try:
        if "date" in pd_data.columns:
            pd_data.set_index("date", inplace=True)
        elif "timestamp" in pd_data.columns:
            pd_data.set_index("timestamp", inplace=True)
    except KeyError:
        raise KeyError("No date or timestamp column found in data.")

    pd_data.index = pd.to_datetime(pd_data.index)
    return xr.Dataset.from_dataframe(pd_data)
