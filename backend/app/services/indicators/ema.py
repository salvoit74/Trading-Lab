class EMA:

    def __init__(self, period):
        self.period = int(period)


    def required_history(self):
        return self.period

    def calculate(self, prices):

        if len(prices) < self.period:
            return None


        multiplier = 2 / (self.period + 1)


        ema = (
            sum(prices[:self.period])
            /
            self.period
        )


        for price in prices[self.period:]:
            ema = (
                (price - ema)
                * multiplier
            ) + ema


        return {
            "value1": ema,
            "value2": None,
            "value3": None
        }
