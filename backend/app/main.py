from flask import Flask, render_template
import psycopg2
import os
from datetime import datetime
from zoneinfo import ZoneInfo
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

logger = logging.getLogger(__name__)



app = Flask(__name__)


# -------------------------------------------------
# Connessione amministrativa per bootstrap
# -------------------------------------------------

def bootstrap_database():

    logger.info("Starting database bootstrap")

    logger.info(
        "Connecting to PostgreSQL as ADMIN host=%s database=%s user=%s",
        os.environ["DB_HOST"],
        os.environ["ADMIN_DB"],
        os.environ["ADMIN_USER"]
    )

    logger.info(
        "Connecting to PostgreSQL as APP host=%s database=%s user=%s",
        os.environ["DB_HOST"],
        os.environ["APP_DB"],
        os.environ["APP_USER"]
    )


    conn = psycopg2.connect(
        host=os.environ["DB_HOST"],
        database=os.environ["ADMIN_DB"],
        user=os.environ["ADMIN_USER"],
        password=os.environ["ADMIN_PASSWORD"]
    )

    logger.info(
        "Connect as %s host=%s database=%s ",
        os.environ["ADMIN_USER"],
        os.environ["DB_HOST"],
        os.environ["ADMIN_DB"],
        
    )

    conn.autocommit = True

    cur = conn.cursor()

    cur.execute("""
      SELECT
      current_user,
      session_user,
      current_database();
      """)

    current_user, session_user, current_db = cur.fetchone()

    logger.info(
      "1.Connected --------------> as current_user=%s session_user=%s database=%s",
      current_user,
      session_user,
      current_db
    )


    db_name = os.environ["APP_DB"]
    app_user = os.environ["APP_USER"]
    app_password = os.environ["APP_PASSWORD"]

    logger.info("Checking database: %s", db_name)
    # Crea database se non esiste
    cur.execute(
        "SELECT 1 FROM pg_database WHERE datname=%s",
        (db_name,)
    )

    if cur.fetchone() is None:
        logger.info("Creating database: %s", db_name)
        cur.execute(
            f"CREATE DATABASE {db_name}"
        )


    logger.info("Checking user %s on DB",app_user)
    
    # Crea utente applicativo se non esiste
    cur.execute(
        "SELECT 1 FROM pg_roles WHERE rolname=%s",
        (app_user,)
    )

    if cur.fetchone() is None:
        logger.info("Creating user %s on DB",app_user)
        cur.execute(
            f"CREATE USER {app_user} PASSWORD '{app_password}'"
        )

    cur.close()
    conn.close()

    conn = psycopg2.connect(
        host=os.environ["DB_HOST"],
        database=os.environ["APP_DB"],
        user=os.environ["ADMIN_USER"],
        password=os.environ["ADMIN_PASSWORD"]
    )

    logger.info(
        "Connect as %s host=%s ",
        os.environ["ADMIN_USER"],
        os.environ["DB_HOST"]
    )

    conn.autocommit = True

    cur = conn.cursor()
    cur.execute("""
      SELECT
      current_user,
      session_user,
      current_database();
      """)

    current_user, session_user, current_db = cur.fetchone()

    logger.info(
      "2.Connected --------------> as current_user=%s session_user=%s database=%s",
      current_user,
      session_user,
      current_db
    )

    db_name = os.environ["APP_DB"]
    app_user = os.environ["APP_USER"]
    app_password = os.environ["APP_PASSWORD"]



    # Assegna permessi sul database
    cur.execute(
        f"GRANT ALL PRIVILEGES ON DATABASE quantica_db TO quantica_usr"
    )
    cur.execute(
        f"GRANT ALL PRIVILEGES ON SCHEMA public TO quantica_usr"
    )

    # Assegna permessi sul database
    cur.execute(
        f"GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {app_user}"
    )
    logger.info("Give GRANT to user %s on DB %s ",app_user,db_name)

    cur.execute(
       f"GRANT USAGE, CREATE ON SCHEMA public TO {app_user}"
    )

    logger.info(
       "Granted USAGE, CREATE on schema public to %s",
       app_user
    )

    cur.execute(
      f"ALTER DEFAULT PRIVILEGES IN SCHEMA public "
      f"GRANT ALL ON TABLES TO {app_user}"
    )

    logger.info(
       "ALTER DEFAULT PRIVILEGES ON TABLES "
    )

    cur.execute(
      f"ALTER DEFAULT PRIVILEGES IN SCHEMA public "
      f"GRANT ALL ON SEQUENCES TO {app_user}"
    )

    logger.info(
       "ALTER DEFAULT PRIVILEGES ON SEQUENCES "
    )


    cur.execute("""
      SELECT
        datname,
        pg_catalog.pg_get_userbyid(datdba) AS owner,
        datacl
      FROM pg_database
      WHERE datname = %s
    """, (db_name,))

    row = cur.fetchone()

    logger.info(
      "Database=%s Owner=%s ACL=%s",
      row[0],
      row[1],
      row[2]
    )    
    
    cur.close()
    conn.close()
    
    logger.info("Database bootstrap completed")



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
            CREATE INDEX idx_market_quotes_symbol_time
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

    print("Quantica bootstrap database...")
    # usa admin_usr
    bootstrap_database()
    print("Initialize application database...")
    # usa quantica_app_usr
    initialize_database()
    print("Starting Quantica Welcome...")

    symbol="AAPL"

    data=get_quote(symbol)

    print(data)



if __name__=="__main__":
    main()