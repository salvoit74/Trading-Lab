from app.services.indicators.sma import SMA


prices = [
    100,
    102,
    104,
    106,
    108
]


indicator = SMA(3)

print(
    indicator.calculate(prices)
)
