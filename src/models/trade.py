
class Trade:
    def __init__(
        self,
        trade_id: str,
        symbol: str,
        side: str,
        price: float,
        quantity: float,
        timestamp: str,
    ) -> None:
        self.trade_id = trade_id
        self.symbol = symbol
        self.side = side
        self.price = price
        self.quantity = quantity
        self.timestamp = timestamp

    def __str__(self) -> str:
        return f"Trade(trade_id={self.trade_id}, symbol={self.symbol}, side={self.side}, price={self.price}, quantity={self.quantity}, timestamp={self.timestamp})"