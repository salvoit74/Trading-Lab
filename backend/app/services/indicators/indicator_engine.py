import logging
from services.indicators.sma import SMA
from services.indicators.ema import EMA
from services.indicators.rsi import RSI
from services.indicators.macd import MACD
from services.indicators.bollinger import BOLLINGER
from datetime import datetime
from zoneinfo import ZoneInfo

from services.indicators.sma import SMA

logger = logging.getLogger(__name__)


class IndicatorEngine:

    def __init__(self, db_connection):
        self.db_connection = db_connection

        #
        # Registered indicators
        #
        self.indicators = {
          "SMA": SMA,
          "EMA": EMA,
          "RSI": RSI,
          "MACD": MACD,
          "BOLLINGER": BOLLINGER
        }

    def calculate_all(
        self,
        symbol
    ):
        """
        Calculate all enabled indicators
        configured for a symbol.
        """
        cur = self.db_connection.cursor()
        cur.execute(
            """
            SELECT
                i.name,
                i.parameters
            FROM symbol_indicators si
            JOIN indicators i
              ON i.id = si.indicator_id
            WHERE
                si.symbol = %s
                AND si.enabled = TRUE
                AND i.enabled = TRUE
            ORDER BY
                i.priority
            """,
            (symbol,)
        )
        rows = cur.fetchall()
        cur.close()
        for row in rows:
            indicator_name = row[0]
            parameters = row[1]
            self.calculate_indicator(
                symbol,
                indicator_name,
                parameters
            )

    def calculate_indicator(
        self,
        symbol,
        indicator_name,
        parameters
    ):
        if indicator_name not in self.indicators:
            logger.warning(
                "Indicator %s not implemented",
                indicator_name
            )
            return
        #
        try:
          indicator_class = self.indicators[indicator_name]
          indicator = indicator_class(parameters)
          prices = self.get_prices(
            symbol,
            indicator.required_history()
          )
          values = indicator.calculate(prices)
        except Exception as e:
          logger.error(
            "Error calculating %s(%s) for %s: %s",
            indicator_name,
            parameters,
            symbol,
            e
          )
          return
        if values is None:
            logger.info(
                "%s(%s) skipped for %s",
                indicator_name,
                parameters,
                symbol
            )
            return
        self.save_indicator(
            symbol,
            indicator_name,
            parameters,
            values
        )
        logger.info(
            "%s %s(%s) = %s",
            symbol,
            indicator_name,
            parameters,
            values
        )

    def get_prices(
        self,
        symbol,
        limit
    ):
        cur = self.db_connection.cursor()
        cur.execute(
            """
            SELECT price
            FROM market_quotes
            WHERE symbol = %s
            ORDER BY quote_time DESC
            LIMIT %s
            """,
            (
                symbol,
                limit
            )
        )
        rows = cur.fetchall()
        cur.close()
        return [
            row[0]
            for row in reversed(rows)
        ]

    def get_last_quote_time(
      self,
      symbol
    ):
      cur = self.db_connection.cursor()
      cur.execute(
        """
        SELECT quote_time
        FROM market_quotes
        WHERE symbol = %s
        ORDER BY quote_time DESC
        LIMIT 1
        """,
        (symbol,)
      )
      row = cur.fetchone()
      cur.close()
      if row:
        return row[0]
      return None

    def save_indicator(
        self,
        symbol,
        indicator,
        parameters,
        values
    ):
        quote_time = self.get_last_quote_time(symbol)
        cur = self.db_connection.cursor()
        cur.execute(
            """
            INSERT INTO indicator_values
            (
                symbol,
                indicator,
                parameters,
                quote_time,
                value1,
                value2,
                value3
            )
            VALUES
            (
                %s,%s,%s,%s,%s,%s,%s
            )
            ON CONFLICT
            (
                symbol,
                indicator,
                parameters,
                quote_time
            )
            DO NOTHING
            """,
            (
                symbol,
                indicator,
                parameters,
                quote_time,
                values.get("value1"),
                values.get("value2"),
                values.get("value3")
            )
        )
        self.db_connection.commit()
        cur.close()
