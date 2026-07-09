from flask import Flask, render_template
import psycopg2
import os
from datetime import datetime
from zoneinfo import ZoneInfo
import logging
import time


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

logger = logging.getLogger(__name__)



app = Flask(__name__)

import time


# -------------------------------------------------
# Lettura titoli monitorati
# -------------------------------------------------

def get_monitored_symbols():
    conn = get_app_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT symbol
        FROM monitored_symbols
        WHERE enabled = TRUE
        ORDER BY symbol
    """)
    symbols = [row[0] for row in cur.fetchall()]
    cur.close()
    conn.close()
    return symbols

# -------------------------------------------------
# Salvataggio quotazione
# -------------------------------------------------

def save_quote(symbol, data):
    conn = get_app_connection()
    cur = conn.cursor()
    logger.info("Save: %s quotation.", symbol )
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

# -------------------------------------------------
# Ciclo raccolta dati
# -------------------------------------------------

def collect_market_quotes():
    symbols = get_monitored_symbols()
    logger.info("Symbols to monitor: %s", symbols )
    for symbol in symbols:
        try:
            logger.info(
                "Request quote for %s",
                symbol
            )
            data = get_quote(symbol)
            logger.info(
                "%s quote received: %s",
                symbol,
                data
            )
            save_quote(
                symbol,
                data
            )
        except Exception as e:
            logger.error("Error processing %s: %s",    symbol,  e  )

# -------------------------------------------------
# Connessione applicativa
# -------------------------------------------------

def get_app_connection():

    return psycopg2.connect(
        host=os.environ["DB_HOST"],
        database=os.environ["APP_DB"],
        user=os.environ["APP_USER"],
        password=os.environ["APP_PASSWORD"]
    )



# -------------------------------------------------
# Tabelle applicative
# -------------------------------------------------

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
      "3.Connected --------------> as current_user=%s session_user=%s database=%s",
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
    """, (datetime.now(ZoneInfo("Europe/Rome")),))

    conn.commit()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS monitored_symbols (
           id SERIAL PRIMARY KEY,
           symbol VARCHAR(20) UNIQUE,
           enabled BOOLEAN DEFAULT TRUE
        )
    """)

    conn.commit()

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



# -------------------------------------------------
# Pagina Welcome
# -------------------------------------------------

@app.route("/")
def welcome():

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
      "4.Connected --------------> as current_user=%s session_user=%s database=%s",
      current_user,
      session_user,
      current_db
    )



    cur.execute("""
        SELECT startup_time
        FROM quantica_log
        ORDER BY id DESC
        LIMIT 1
    """)

    startup = cur.fetchone()[0]

    cur.close()
    conn.close()

    giorni = [
      "lunedì",
      "martedì",
      "mercoledì",
      "giovedì",
      "venerdì",
      "sabato",
      "domenica"
    ]

    startup_local = startup.astimezone(ZoneInfo("Europe/Rome"))
    text = startup_local.strftime(
      "La piattaforma è attiva dalle %H:%M:%S di "
    ) + f"{giorni[startup_local.weekday()]} {startup_local.strftime('%d/%m/%Y')}"

    return render_template(
        "index.html",
        startup_text=text
    )



# -------------------------------------------------
# ENTRY POINT CONTAINER
# -------------------------------------------------

from finnhub_client import get_quote


def main():
    print("Initialize application database...")
    initialize_database()
    print("Starting Trading LAB Welcome...")

# Inizio Attivita'
    logger.info( "Market collection Starting"   )
    for cycle in range(1, 11):
        logger.info(
            "===== Market collection cycle %s/10 =====",
            cycle
        )
        collect_market_quotes()
        if cycle < 10:
            logger.info(
                "Waiting 5 minutes before next cycle..."
            )
            time.sleep(300)
    logger.info("Market collection completed")

if __name__=="__main__":
    main()
