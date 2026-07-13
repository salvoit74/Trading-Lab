from flask import Flask, render_template
import logging
import time

from services.market_data_service import MarketDataService
from database.initializer import initialize_database

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

logger = logging.getLogger(__name__)

app = Flask(__name__)


# -------------------------------------------------
# ENTRY POINT CONTAINER
# -------------------------------------------------


def main():
    logger.info("Initialize application database...")
    initialize_database()
    logger.info("Starting Trading LAB Welcome...")

# Inizio Attivita'
    logger.info( "Market collection Starting"   )
    market_service = MarketDataService()
    for cycle in range(1, 11):
        logger.info(
            "===== Market collection cycle %s/10 =====",
            cycle
        )
        market_service.collect_quotes()
        if cycle < 10:
            logger.info(
                "Waiting 5 minutes before next cycle..."
            )
            time.sleep(300)
    logger.info("Market collection completed")

if __name__=="__main__":
    main()
