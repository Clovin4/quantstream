import typing

import json

import numpy as np
import pandas as pd
import xarray as xr

from .technical_indictors import technical_indicators
from .technicals import daily, intraday, quote


def json_to_xarray(data: list[dict]) -> xr.Dataset:
    """Convert json data to xarray."""
    return FinDataset.from_json(data)


class FinDataset(xr.Dataset):
    __slots__ = ()

    def __init__(
        self,
        data_vars=None,
        coords=None,
        attrs=None,
    ):
        super().__init__(data_vars, coords, attrs)

    @property
    def name(self):
        return self.attrs.get("name")

    @name.setter
    def name(self, value):
        self.attrs["name"] = value

    @classmethod
    def from_json(cls, data: list[dict]) -> "FinDataset":
        """Create a FinDataset from a list of dictionaries."""
        cols = data[0].keys()

        raw_data = {col: [row[col] for row in data] for col in cols}

        if "date" in raw_data:
            index = np.array(raw_data.pop("date"), dtype="datetime64")
        elif "timestamp" in raw_data:
            index = np.array(raw_data.pop("timestamp"), dtype="datetime64")
        else:
            raise KeyError("No date or timestamp column found in data.")

        data_vars = {
            col: xr.DataArray(raw_data[col], dims="time", coords={"time": index})
            for col in raw_data.keys()
        }

        return cls(data_vars)

    @classmethod
    def from_dataframe(cls, data: pd.DataFrame) -> "FinDataset":
        """Create a FinDataset from a pandas DataFrame."""
        return xr.Dataset.from_dataframe(data)

    def to_json(self) -> list[dict]:
        """Convert the FinDataset to a list of dictionaries."""
        return json.loads(self.to_dataframe().to_json(orient="records"))

    def to_dataframe(self) -> pd.DataFrame:
        """Convert the FinDataset to a pandas DataFrame."""
        return self.to_dataframe()
