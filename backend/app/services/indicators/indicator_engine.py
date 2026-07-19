import logging

from datetime import datetime
from zoneinfo import ZoneInfo

from app.services.indicators.sma import SMA

logger = logging.getLogger(__name__)


class IndicatorEngine:

    def __init__(self, db_connection):
        self.db_connection = db_connection

        #
        # Registered indicators
        #
        self.indicators = {
            "SMA": SMA
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
        # only one parameter for SMA
        #
        period = int(parameters)
        prices = self.get_prices(
            symbol,
            period
        )
        indicator = self.indicators[indicator_name](
            period
        )
        value = indicator.calculate(
            prices
        )
        if value is None:
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
            value
        )
        logger.info(
            "%s(%s) = %.4f",
            indicator_name,
            parameters,
            value
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

    def save_indicator(
        self,
        symbol,
        indicator,
        parameters,
        value
    ):
        cur = self.db_connection.cursor()
        cur.execute(
            """
            INSERT INTO indicator_values
            (
                symbol,
                indicator,
                parameters,
                quote_time,
                value1
            )
            VALUES
            (
                %s,%s,%s,%s,%s
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
                datetime.now(
                    ZoneInfo("UTC")
                ),
                value
            )
        )
        self.db_connection.commit()
        cur.close()
