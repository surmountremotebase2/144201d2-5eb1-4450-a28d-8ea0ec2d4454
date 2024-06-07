from surmount.base_class import Strategy, TargetAllocation
from surmount.data import Asset, OHLCV
from surmount.technical_indicators import VWAP
from surmount.logging import log
import pandas as pd

class TradingStrategy(Strategy):
    def __init__(self):
        # Setup initial parameters
        self.ticker = "GME"
        # Example reversal points (in reality, these should be dynamically identified)
        self.reversal_dates = ["YYYY-MM-DD", "YYYY-MM-DD"]  # Placeholder dates
        self.data_list = [OHLCV(self.ticker)]

    @property
    def interval(self):
        # 15-minutes timeframe
        return "15min"

    @property
    def assets(self):
        return [self.ticker]

    @property
    def data(self):
        return self.data_list

    def run(self, data):
        ohlcv = data["ohlcv"]
        current_price = ohlcv[-1][self.ticker]["close"]
        
        # Example of how to calculate an anchored VWAP from a selected reversal date.
        # You would iterate over reversal_dates to find the relevant one for current conditions.
        # Here, simplified to use the latest data available.
        vwap_values = self.calculate_anchored_vwap(self.ticker, ohlcv, self.reversal_dates[-1])

        if not vwap_values:
            return TargetAllocation({})

        last_vwap = vwap_values[-1]

        # Decide to buy if current price is above the anchored VWAP and sell if below.
        # This is a simplification; more complex logic and risk management should be applied.
        if current_price > last_vwap:
            allocation = {"GME": 1.0}  # Full allocation to GME
        else:
            allocation = {"GME": 0}  # No allocation to GME

        return TargetAllocation(allocation)

    def calculate_anchored_vwap(self, ticker, ohlcv, anchor_date):
        """
        Calculate the anchored VWAP from a specific anchor date.
        This is a simplified example function. Actual implementation may vary based
        on available data and how dates are handled.
        """
        # Filter data since the anchor_date
        filtered_data = [point for point in ohlcv if point[ticker]["date"] >= anchor_date]
        if not filtered_data:
            log(f"No data available after anchor date {anchor_date}")
            return None

        # Collect high, low, close, and volume for VWAP calculation
        high = pd.Series([point[ticker]["high"] for point in filtered_data])
        low = pd.Series([point[ticker]["low"] for point in filtered_data])
        close = pd.Series([point[ticker]["close"] for point in filtered_data])
        volume = pd.Series([point[ticker]["volume"] for point in filtered_data])

        # Simulate VWAP calculation - note, we assume a VWAP function that supports anchoring, which may not be directly available
        # and would need to be implemented.
        vwap = VWAP(ticker, filtered_data, len(filtered_data))  # Simplified; actual implementation needed

        if vwap is None:
            log("Failed to calculate VWAP.")
            return None

        return vwap