import logging
from datetime import datetime
from zoneinfo import ZoneInfo

from database.initializer import get_app_connection
from finnhub_client import FinnhubProvider


logger = logging.getLogger(__name__)


class MarketDataService:

    def __init__(self):
        self.provider = FinnhubProvider()


    def collect_quotes(self):

        symbols = self.get_monitored_symbols()

        logger.info(
            "Symbols to monitor: %s",
            symbols
        )

        for symbol in symbols:

            try:

                logger.info(
                    "Request quote for %s",
                    symbol
                )

                quote = self.provider.get_quote(symbol)


                logger.info(
                    "%s quote received: %s",
                    symbol,
                    quote
                )


                self.save_quote(
                    symbol,
                    quote
                )


            except Exception as e:

                logger.error(
                    "Error processing %s: %s",
                    symbol,
                    e
                )



    def get_monitored_symbols(self):

        conn = get_app_connection()

        cur = conn.cursor()

        cur.execute("""
            SELECT symbol
            FROM monitored_symbols
            WHERE enabled = TRUE
            ORDER BY symbol
        """)

        symbols = [
            row[0]
            for row in cur.fetchall()
        ]

        cur.close()
        conn.close()

        return symbols



    def save_quote(
        self,
        symbol,
        data
    ):

        import psycopg2
        import os


        conn = psycopg2.connect(
            host=os.environ["DB_HOST"],
            database=os.environ["APP_DB"],
            user=os.environ["APP_USER"],
            password=os.environ["APP_PASSWORD"]
        )


        cur = conn.cursor()


        cur.execute("""
            INSERT INTO market_quotes (
                symbol,
                quote_time,
                price,
                change_value,
                change_percent,
                day_high,
                day_low,
                day_open,
                previous_close
            )
            VALUES (
                %s,%s,%s,%s,%s,%s,%s,%s,%s
            )
        """,
        (
            symbol,
            datetime.now(ZoneInfo("UTC")),
            data.get("c"),
            data.get("d"),
            data.get("dp"),
            data.get("h"),
            data.get("l"),
            data.get("o"),
            data.get("pc")
        ))


        conn.commit()

        cur.close()
        conn.close()
