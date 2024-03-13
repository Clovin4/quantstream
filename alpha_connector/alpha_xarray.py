import json

import xarray as xr


def json_to_xarray(json_data):
    # Load JSON data
    data = json.loads(json_data)

    # Convert JSON data to xarray dataset
    dataset = xr.Dataset.from_dict(data)

    return dataset
