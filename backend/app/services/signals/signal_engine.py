from app.services.signals.ema_cross import EMACross
from app.services.signals.rsi_signal import RSISignal
from app.services.signals.macd_signal import MACDSignal


class SignalEngine:

    def __init__(self, db):

        self.db = db

        self.signals = {
            "EMA_CROSS": EMACross(db),
            "RSI": RSISignal(db),
            "MACD": MACDSignal(db),
        }

    def calculate_signal(
        self,
        symbol,
        signal_name,
        parameters
    ):

        if signal_name not in self.signals:
            return None

        return self.signals[signal_name].calculate(
            symbol,
            parameters
        )
