class RSI:

    def __init__(self, period):
        self.period = int(period)

    def required_history(self):
        return self.period + 1

    def calculate(self, prices):

        if len(prices) <= self.period:
            return None


        gains = []
        losses = []


        for i in range(1, len(prices)):

            change = prices[i] - prices[i-1]

            if change >= 0:
                gains.append(change)
                losses.append(0)

            else:
                gains.append(0)
                losses.append(abs(change))


        avg_gain = (
            sum(gains[:self.period])
            /
            self.period
        )

        avg_loss = (
            sum(losses[:self.period])
            /
            self.period
        )


        if avg_loss == 0:
            rsi = 100

        else:

            rs = avg_gain / avg_loss

            rsi = 100 - (
                100 /
                (1 + rs)
            )


        return {
            "value1": rsi,
            "value2": None,
            "value3": None
        }
