"""Url patterns for the FMP API."""


class FMP_URLS:
    """Base class for FMP API."""

    def __init__(self, response_format: str = "json") -> None:
        self.response_format = response_format

        self.base_url_v3 = "https://financialmodelingprep.com/api/v3/"
        self.base_url_v4 = "https://financialmodelingprep.com/api/v4/"

        # default values
        self.default_limit = 100
        self.default_line_param = "line"

        # time delta values
        self.time_delta_values = [
            "1min",
            "5min",
            "15min",
            "30min",
            "1hour",
            "4hour",
        ]
        self.technical_indicator_time_delta_values = [
            "1min",
            "5min",
            "15min",
            "30min",
            "1hour",
            "4hour",
            "daily",
        ]
        self.statistics_type_values = [
            "sma",
            "ema",
            "wma",
            "dema",
            "tema",
            "williams",
            "rsi",
            "adx",
            "standardDeviation",
        ]
