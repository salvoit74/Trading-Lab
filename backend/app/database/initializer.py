import logging
from datetime import datetime
from zoneinfo import ZoneInfo

import psycopg2
import os


logger = logging.getLogger(__name__)


def get_app_connection():

    return psycopg2.connect(
        host=os.environ["DB_HOST"],
        database=os.environ["APP_DB"],
        user=os.environ["APP_USER"],
        password=os.environ["APP_PASSWORD"]
    )


def initialize_database():

    conn = get_app_connection()
    cur = conn.cursor()


    cur.execute("""
      SELECT
      current_user,
      session_user,
      current_database();
    """)

    current_user, session_user, current_db = cur.fetchone()

    logger.info(
        "Connected as current_user=%s session_user=%s database=%s",
        current_user,
        session_user,
        current_db
    )


    cur.execute("""
        CREATE TABLE IF NOT EXISTS trading_log (
            id SERIAL PRIMARY KEY,
            startup_time TIMESTAMP NOT NULL
        )
    """)


    cur.execute("""
        INSERT INTO trading_log(startup_time)
        VALUES (%s)
    """,
    (
        datetime.now(
            ZoneInfo("Europe/Rome")
        ),
    ))


    cur.execute("""
        CREATE TABLE IF NOT EXISTS monitored_symbols (
           id SERIAL PRIMARY KEY,
           symbol VARCHAR(20) UNIQUE,
           enabled BOOLEAN DEFAULT TRUE
        )
    """)


    cur.execute("""
        CREATE TABLE IF NOT EXISTS market_quotes (
           id BIGSERIAL PRIMARY KEY,
           symbol VARCHAR(20) NOT NULL,
           quote_time TIMESTAMP WITH TIME ZONE NOT NULL,
           price NUMERIC(18,6) NOT NULL,
           change_value NUMERIC(18,6),
           change_percent NUMERIC(10,6),
           day_high NUMERIC(18,6),
           day_low NUMERIC(18,6),
           day_open NUMERIC(18,6),
           previous_close NUMERIC(18,6),
           source VARCHAR(50) DEFAULT 'FINNHUB',
           created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        )
    """)


    cur.execute("""
      CREATE INDEX IF NOT EXISTS idx_market_quotes_symbol_time
      ON market_quotes(symbol, quote_time DESC);
    """)


    conn.commit()

    cur.close()
    conn.close()

    logger.info(
        "Database initialization completed"
    )
