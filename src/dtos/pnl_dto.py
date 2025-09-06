from dataclasses import dataclass
from typing import List, Optional


@dataclass
class RealizedPnLDto:
    symbol: str
    total_realized_pnl: float
    note: Optional[str] = None


@dataclass
class UnrealizedPnLDto:
    symbol: str
    quantity: float
    average_price: float
    current_price: float
    unrealized_pnl: float

    def to_dict(self) -> dict:
        return {
            "symbol": self.symbol,
            "quantity": self.quantity,
            "average_price": self.average_price,
            "current_price": self.current_price,
            "unrealized_pnl": self.unrealized_pnl
        }


@dataclass
class CombinedPnLDto:
    symbol: str
    quantity: float
    average_price: float
    current_price: float
    unrealized_pnl: float
    realized_pnl: float
    total_pnl: float

    def to_dict(self) -> dict:
        return {
            "symbol": self.symbol,
            "quantity": self.quantity,
            "average_price": self.average_price,
            "current_price": self.current_price,
            "unrealized_pnl": self.unrealized_pnl,
            "realized_pnl": self.realized_pnl,
            "total_pnl": self.total_pnl
        }


@dataclass
class PnLSummaryDto:
    pnl: List[CombinedPnLDto]
    total_unrealized_pnl: float
    total_realized_pnl: float
    total_pnl: float
    count: int

    def to_dict(self) -> dict:
        return {
            "pnl": [item.to_dict() for item in self.pnl],
            "total_unrealized_pnl": self.total_unrealized_pnl,
            "total_realized_pnl": self.total_realized_pnl,
            "total_pnl": self.total_pnl,
            "count": self.count
        }
