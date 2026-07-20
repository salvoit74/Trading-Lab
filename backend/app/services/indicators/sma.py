class SMA:
    """
    Simple Moving Average
    """

    def __init__(self, period):
        self.period = int(period)

    def required_history(self):
        return self.period

    def calculate(self, prices):
        if len(prices) < self.period:
            return None
        value = sum(
            prices[-self.period:]
        ) / self.period
        return {
            "value1": value,
            "value2": None,
            "value3": None
        }
