import os
import subprocess
import logging
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

BASE_PATH = "/srv/projects/Quantica/backend/apps/trading-lab/app/database/schema"

STRUCTURE_FILE = os.path.join(
    BASE_PATH,
    "001_tables.sql"
)

INDEX_FILE = os.path.join(
    BASE_PATH,
    "002_indexes.sql"
)

SEED_FILE = os.path.join(
    BASE_PATH,
    "003_seed.sql"
)


def run_pg_dump(args, output_file):

    logger.info(
        "Exporting %s",
        output_file
    )
    env = os.environ.copy() 
    env["PGPASSWORD"] = os.environ["APP_PASSWORD"]
    with open(
        output_file,
        "w"
    ) as f:
        subprocess.run(
            args,
            stdout=f,
            stderr=subprocess.PIPE,
            check=True,
            text=True,
            env=env
        )

def export_structure():

    os.makedirs(
        BASE_PATH,
        exist_ok=True
    )

    db_host = os.environ["DB_HOST"]
    db_name = os.environ["APP_DB"]
    db_user = os.environ["APP_USER"]
    db_password= os.environ["APP_PASSWORD"]


    #
    # 001 - TABLES
    #
    run_pg_dump(
        [
            "pg_dump",
            "-w",
            "-h",
            db_host,
            "-U",
            db_user,
            "-d",
            db_name,
            "--schema-only",
            "--section=pre-data"
        ],
        STRUCTURE_FILE
    )


    #
    # 002 - INDEXES AND CONSTRAINTS
    #
    run_pg_dump(
        [
            "pg_dump",
            "-h",
            db_host,
            "-U",
            db_user,
            "-d",
            db_name,
            "--schema-only",
            "--section=post-data"
        ],
        INDEX_FILE
    )


    #
    # 003 - INITIAL DATA
    #
    run_pg_dump(
        [
            "pg_dump",
            "-h",
            db_host,
            "-U",
            db_user,
            "-d",
            db_name,
            "--data-only",
            "--table=indicators",
            "--table=monitored_symbols",
            "--table=symbol_indicators",
            "--table=maintenance_tasks"
        ],
        SEED_FILE
    )


    logger.info(
        "Database export completed at %s",
        datetime.now()
    )


if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s"
    )

    export_structure()
