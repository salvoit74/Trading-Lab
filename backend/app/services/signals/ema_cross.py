class EMACross(BaseSignal):

    def calculate(
        self,
        symbol,
        parameters
    ):

        fast = parameters["fast"]
        slow = parameters["slow"]

        ema_fast = self.db.get_indicator_value(
            symbol,
            "EMA",
            fast
        )

        ema_slow = self.db.get_indicator_value(
            symbol,
            "EMA",
            slow
        )

        if ema_fast > ema_slow:
            signal = "BUY"
        elif ema_fast < ema_slow:
            signal = "SELL"
        else:
            signal = "HOLD"

        self.db.save_signal(
            symbol,
            "EMA_CROSS",
            parameters,
            signal
        )

        return signal
