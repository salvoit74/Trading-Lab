
from decimal import Decimal
import logging
logger = logging.getLogger(__name__)

class EMA:

    def __init__(self, period):
        self.period = int(period)

    def required_history(self):
        return max(self.period * 5, 100)

    def calculate(self, prices):
        if len(prices) < self.period:
            return None
        multiplier = 2 / (self.period + 1)
        multiplier =Decimal(str(multiplier))
        ema = (
            sum(prices[:self.period])
            /
            self.period
        )
        ema =Decimal(str(ema))
        for price in prices[self.period:]:
            ema = (
                (price - ema)
                * multiplier
            ) + ema
            ema =Decimal(str(ema))
        return {
            "value1": ema,
            "value2": None,
            "value3": None
        }
