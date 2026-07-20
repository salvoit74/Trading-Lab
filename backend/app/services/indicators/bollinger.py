import statistics


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


        stddev = statistics.stdev(
            values
        )


        upper = (
            middle
            +
            self.deviation * stddev
        )


        lower = (
            middle
            -
            self.deviation * stddev
        )


        return {
            "value1": middle,
            "value2": upper,
            "value3": lower
        }
