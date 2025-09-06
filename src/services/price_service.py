class PriceService:
    def __init__(self):
        self.prices = {
            "BTC": 10000,
            "ETH": 2000,
            "XRP": 1,
            "SOL": 100,
            "DOGE": 0.1,
            "SHIB": 0.0001,
            "DOT": 10,
        }

    def get_price(self, symbol: str) -> float:
        return self.prices[symbol]