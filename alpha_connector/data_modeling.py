import json

import numpy as np
import pandas as pd
import xarray as xr


def verify_json(data):
    if "Error Message" in data:
        raise ValueError(data["Error Message"])
    elif "Information" in data:
        raise ValueError(data["Information"])
    elif "Note" in data:
        raise ValueError(data["Note"])
    else:
        return True


def json_to_xarray(data, interval):

    dates = np.array(
        list(data[f"Time Series ({interval})"].keys())[:], dtype="datetime64[s]"
    )

    data_x = np.array(list(data[f"Time Series ({interval})"].values())[:])

    attrs = data["Meta Data"]

    # Create a structured array
    dtype = [
        ("open", "f4"),
        ("high", "f4"),
        ("low", "f4"),
        ("close", "f4"),
        ("volume", "i8"),
    ]

    structured_data = np.array([tuple(d.values()) for d in data_x], dtype=dtype)

    # Convert to a pandas DataFrame for easy conversion to xarray
    df = pd.DataFrame(structured_data, index=pd.to_datetime(dates))

    # Convert the pandas DataFrame to an xarray Dataset
    ds = xr.Dataset.from_dataframe(df)
    # Add the attributes
    ds.attrs = attrs

    return ds
