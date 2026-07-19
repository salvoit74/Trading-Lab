from flask import Flask, render_template
import logging
import time

from services.market_data_service import MarketDataService
from database.initializer import initialize_database
from services.maintenance.maintenance_service import MaintenanceService

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
    maintenance_service = MaintenanceService()
    INTERVAL = 65
    while True:
      logger.info( "===== Market collection cycle =====",)
      start = time.time()
      market_service.collect_quotes()
      maintenance_service.run()
      elapsed = time.time() - start
      wait = max(0, INTERVAL - elapsed)
      time.sleep(wait)

if __name__=="__main__":
    main()
