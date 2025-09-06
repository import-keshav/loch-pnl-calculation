from src.services.trade_service import TradeService
from src.services.portfolio_service import PortfolioService
from src.models.trade import Trade


class TradeManager:
    def __init__(
        self, trade_service: TradeService, 
        portfolio_service: PortfolioService
    ):
        self.trade_service = trade_service
        self.portfolio_service = portfolio_service

    def add_trade(self, trade: Trade):
        try:
            self.trade_service.add_trade(trade)
        except Exception as e:
            print(f"Error adding trade: {e}")
            raise Exception(f"Error adding trade: {e}")

        try:
            self.portfolio_service.add_trade(trade)
        except Exception as e:
            print(f"Error adding trade to portfolio: {e}")
            raise Exception(f"Error adding trade to portfolio: {e}")