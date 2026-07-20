class MACD:
    """
    Moving Average Convergence Divergence
    Parameters:
        fast_period
        slow_period
        signal_period
    """

    def __init__(self, parameters):
        values = parameters.split(",")
        self.fast_period = int(values[0])
        self.slow_period = int(values[1])
        self.signal_period = int(values[2])

    def required_history(self):
        return self.slow_period + self.signal_period

    def calculate_ema(
        self,
        prices,
        period
    ):
        if len(prices) < period:
            return None
        multiplier = 2 / (period + 1)
        ema = (
            sum(prices[:period])
            /
            period
        )
        for price in prices[period:]:
            ema = (
                (price - ema)
                * multiplier
            ) + ema
        return ema

    def calculate(
        self,
        prices
    ):
        if len(prices) < self.slow_period + self.signal_period:
            return None
        macd_values = []
        for index in range(
            self.slow_period,
            len(prices)+1
        ):
            slice_prices = prices[:index]
            fast = self.calculate_ema(
                slice_prices,
                self.fast_period
            )
            slow = self.calculate_ema(
                slice_prices,
                self.slow_period
            )
            if fast is not None and slow is not None:
                macd_values.append(
                    fast - slow
                )
        if len(macd_values) < self.signal_period:
            return None
        macd_line = macd_values[-1]
        signal_line = self.calculate_ema(
            macd_values,
            self.signal_period
        )
        histogram = (
            macd_line - signal_line
        )
        return {
            "value1": macd_line,
            "value2": signal_line,
            "value3": histogram
        }
