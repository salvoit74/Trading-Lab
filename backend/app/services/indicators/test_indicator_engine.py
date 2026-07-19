import psycopg2
import os

from dotenv import load_dotenv
from app.services.indicators.indicator_engine import IndicatorEngine

load_dotenv()

conn = psycopg2.connect(
  host=os.environ["DB_HOST"],
  database=os.environ["APP_DB"],
  user=os.environ["APP_USER"],
  password=os.environ["APP_PASSWORD"]
)
engine = IndicatorEngine(conn)
result = engine.calculate_sma(
    "AAPL",
    20
)
print(
    f"SMA result: {result}"
)

conn.close()
