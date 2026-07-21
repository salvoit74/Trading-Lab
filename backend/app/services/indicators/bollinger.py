import statistics
from decimal import Decimal

class BOLLINGER:
    """
    Bollinger Bands

    Parameters:
        period,deviation
    """


    def __init__(self, parameters):

        values = parameters.split(",")

        self.period = int(values[0])
        self.deviation = float(values[1])

    def required_history(self):

        return self.period


    def calculate(
        self,
        prices
    ):

        if len(prices) < self.period:
            return None


        values = prices[-self.period:]


        middle = (
            sum(values)
            /
            self.period
        )
        middle=Decimal(str(middle))


        stddev = statistics.stdev(
            values
        )
        stddev=Decimal(str(stddev))

        deviation=Decimal(str(self.deviation))
        upper = (
            middle
            +
            deviation * stddev
        )


        lower = (
            middle
            -
            deviation * stddev
        )


        return {
            "value1": middle,
            "value2": upper,
            "value3": lower
        }
