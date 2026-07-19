import logging
from datetime import datetime
from zoneinfo import ZoneInfo
from decimal import Decimal

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
                current_price = Decimal(str(quote.get("c")))
                last_price = self.get_last_price(symbol)
                if last_price != current_price:
                  logger.info(
                    "%s cambio di prezzo %s <> %s",
                    symbol,
                    last_price,
                    current_price
                  )
                  self.save_quote(symbol, quote)
                self.update_symbol_execution(
                  symbol,
                  current_price
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
              AND (
                last_execution IS NULL
                OR last_execution <= NOW() - (interval_seconds * INTERVAL '1 second')
              )
            ORDER BY last_execution asc ,priority, symbol
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
        
        provider_time = None
        if data.get("t"):
          provider_time = datetime.fromtimestamp(
            data.get("t"),
            tz=ZoneInfo("UTC")
          )

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
                provider_quote_time,
                price,
                change_value,
                change_percent,
                day_high,
                day_low,
                day_open,
                previous_close
            )
            VALUES (
                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s
            )
        """,
        (
            symbol,
            datetime.now(ZoneInfo("UTC")),
            provider_time,
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
    
    def update_symbol_execution(
      self,
      symbol,
      last_price
    ):
      import psycopg2
      import os
      conn = psycopg2.connect(
        host=os.environ["DB_HOST"],
        database=os.environ["APP_DB"],
        user=os.environ["APP_USER"],
        password=os.environ["APP_PASSWORD"]
      )
      logger.info(
          "Symbols to Update Execution time on: %s",
          symbol
      )
      cur = conn.cursor()
      cur.execute("""
        UPDATE monitored_symbols
           SET last_execution = %s,
               last_price = %s
         WHERE symbol = %s
        """,
        (
          datetime.now(ZoneInfo("UTC")),
          last_price,
          symbol
        ))
      conn.commit()
      cur.close()
      conn.close()

    def get_last_price(
      self,
      symbol
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
        SELECT last_price
        FROM monitored_symbols
        WHERE symbol = %s
      """, (symbol,))
      row = cur.fetchone()
      cur.close()
      conn.close()
      if row is None:
        return None
      return row[0]
