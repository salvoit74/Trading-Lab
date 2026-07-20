import logging
from datetime import datetime
from zoneinfo import ZoneInfo

import psycopg2
import os


logger = logging.getLogger(__name__)

REQUIRED_TABLES = [
    "monitored_symbols",
    "market_quotes",
    "indicators",
    "symbol_indicators",
    "indicator_values",
    "database_info",
    "maintenance_tasks"
]

def database_exists(conn):
    """
    Returns True only if all required Trading-Lab tables exist.
    """

    cur = conn.cursor()

    cur.execute(
        """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
          AND table_name = ANY(%s)
        """,
        (REQUIRED_TABLES,)
    )

    existing_tables = {row[0] for row in cur.fetchall()}
    cur.close()

    missing_tables = [
        table
        for table in REQUIRED_TABLES
        if table not in existing_tables
    ]

    if missing_tables:
        logger.warning(
            "Database not initialized. Missing tables: %s",
            ", ".join(missing_tables)
        )
        return False

    logger.info(
        "All required Trading-Lab tables are present."
    )

    return True

def get_app_connection():

    return psycopg2.connect(
        host=os.environ["DB_HOST"],
        database=os.environ["APP_DB"],
        user=os.environ["APP_USER"],
        password=os.environ["APP_PASSWORD"]
    )


def initialize_database():
    conn = get_app_connection()
    logger.info(
       "Database test initialized"
    )
    if database_exists(conn):
        logger.info(
            "Database already initialized"
        )
        return
    execute_sql_file(
        conn,
        "schema/001_tables.sql"
    )
    execute_sql_file(
        conn,
        "schema/002_indexes.sql"
    )
    execute_sql_file(
        conn,
        "schema/003_seed.sql"
    )
    logger.info(
        "Database initialization completed"
    )
