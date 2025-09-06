from src.models.trade import Trade
from typing import List, Optional

class TradeService:
    def __init__(self):
        self.trades = []

    def add_trade(self, trade: Trade):
        self.trades.append(trade)

    def get_trades(self):
        return self.trades

    def get_trades_by_symbol_and_side(self, symbol: str, side: Optional[str] = None) -> List[Trade]:
        filtered_trades = []
        
        for trade in self.trades:
            if trade.symbol == symbol:
                if side is None or trade.side == side:
                    filtered_trades.append(trade)
        
        return filtered_trades
