class SMA:
    """
    Simple Moving Average indicator
    """

    def __init__(self, period):
        self.period = period


    def calculate(self, prices):
        """
        Calculate SMA.

        prices:
            list of numeric values ordered oldest -> newest
        """

        if len(prices) < self.period:
            return None

        values = prices[-self.period:]

        return sum(values) / self.period
