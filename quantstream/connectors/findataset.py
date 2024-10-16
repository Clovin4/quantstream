import numpy as np
import xarray as xr
import plotly.graph_objects as go


class FinDataset(xr.Dataset):
    """_summary_

    Args:
        xr (_type_): _description_

    Raises:
        KeyError: _description_

    Returns:
        _type_: _description_
    """

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
        """
        str: The name of the dataset.
        """
        return self.attrs.get("name")

    @name.setter
    def name(self, value):
        self.attrs["name"] = value

    @classmethod
    def from_json(cls, data):
        """_summary_

        Args:
            data (_type_): _description_

        Raises:
            KeyError: _description_

        Returns:
            _type_: _description_
        """
        cols = data[0].keys()

        raw_data = {col: [row[col] for row in data] for col in cols}

        if "date" in raw_data:
            index = np.array(raw_data.pop("date"), dtype="datetime64[ns]")
        elif "timestamp" in raw_data:
            index = np.array(raw_data.pop("timestamp"), dtype="datetime64[ns]")
        else:
            raise KeyError("No date or timestamp column found in data.")

        data_vars = {
            col: xr.DataArray(raw_data[col], dims="time", coords={"time": index})
            for col in raw_data.keys()
        }

        return cls(data_vars)

    def plot_candlestick(
        self, from_date: np.datetime64 = None, to_date: np.datetime64 = None
    ):
        """
        Plot a candlestick chart.
        """

        if to_date is None:
            to_date = self["close"].time[-1]

        if from_date is None:
            from_date = self["close"].time[-1] - np.timedelta64(14, "D")

        data = self.sel(time=slice(from_date, to_date))

        fig = go.Figure(
            data=[
                go.Candlestick(
                    x=data.time,
                    open=data.open,
                    high=data.high,
                    low=data.low,
                    close=data["close"],
                    name="Candlestick",
                )
            ]
        )

        fig.show()
