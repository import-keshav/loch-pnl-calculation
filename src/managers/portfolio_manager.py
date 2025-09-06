from src.services.portfolio_service import PortfolioService
from src.models.trade import Trade


class PortfolioManager:
    def __init__(self, portfolio_service: PortfolioService):
        self.portfolio_service = portfolio_service

    def add_trade(self, trade: Trade):
        self.portfolio_service.add_trade(trade)
    
    def get_portfolio(self):
        holdings = self.portfolio_service.get_holdings()
        portfolio_list = []
        
        for symbol, data in holdings.items():
            portfolio_list.append({
                "symbol": symbol,
                "quantity": data["quantity"],
                "average_price": data["average_price"]
            })
        
        return portfolio_list