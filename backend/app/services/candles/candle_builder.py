from decimal import Decimal


class CandleBuilder:

    def build(
        self,
        symbol,
        timeframe,
        candle_time,
        quotes
    ):
        """
        Costruisce una candela OHLC.

        quotes deve essere ordinata cronologicamente
        (dal più vecchio al più recente).
        """

        if not quotes:
            return None

        prices = [
            quote["price"]
            for quote in quotes
        ]

        return {

            "symbol": symbol,

            "timeframe": timeframe,

            "candle_time": quotes[0]["quote_time"],

            "open_price": prices[0],

            "high_price": max(prices),

            "low_price": min(prices),

            "close_price": prices[-1]

        }
