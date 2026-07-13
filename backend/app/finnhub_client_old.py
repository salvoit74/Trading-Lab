import os
import requests


FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")


def get_quote(symbol):

    if not FINNHUB_API_KEY:
        raise Exception("FINNHUB_API_KEY missing")

    print(f"Using Finnhub key: {FINNHUB_API_KEY[:5]}*****")

    url = "https://finnhub.io/api/v1/quote"

    params = {
        "symbol": symbol,
        "token": FINNHUB_API_KEY
    }

    response = requests.get(url, params=params)

    response.raise_for_status()

    return response.json()