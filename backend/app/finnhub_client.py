

import finnhub
from config import FINNHUB_API_KEY

class FinnhubProvider:

    def __init__(self, api_key=None):
        if api_key is None:
            api_key = FINNHUB_API_KEY
        self.client = finnhub.Client(api_key=api_key)

    def get_quote(self, symbol):
        return self.client.quote(symbol)

    def get_company_profile(self, symbol):
        return self.client.company_profile2(symbol=symbol)

    def get_candles(self, symbol, resolution, start, end):
        return self.client.stock_candles(
            symbol,
            resolution,
            start,
            end
        )
