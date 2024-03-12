import logging
import os

import dotenv
import numpy as np
import pandas as pd
import requests
import xarray as xr

dotenv.load_dotenv()

API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

# log to txt file
logging.basicConfig(filename="plutus.log", level=logging.DEBUG)


class AlphaVantage:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://www.alphavantage.co/query?"

    def get_data(self, function, interval, symbol):
        url = f"{self.base_url}function={function}&symbol={symbol}&interval={interval}&apikey={self.api_key}"
        logging.info(f"Requesting data from {url}")
        r = requests.get(url)
        data = r.json()
        # logging.info(f"Data received: {data}")

        # Convert data to xarray here
        # This will depend on the structure of the data
        # xarray_data = xr.DataArray(data)
        dates = np.array(
            list(data[f"Time Series ({interval})"].keys())[1:], dtype="datetime64[D]"
        )

        data_x = np.array(list(data[f"Time Series ({interval})"].values())[1:])

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


if __name__ == "__main__":
    api_key = API_KEY
    # print("Hello World!")
    av = AlphaVantage(api_key)
    print(av.base_url)
    data = av.get_data("TIME_SERIES_INTRADAY", "5min", "IBM")

    attrs = data.attrs
    print(attrs)
