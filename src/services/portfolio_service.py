from typing import Dict
from src.models.trade import Trade


class PortfolioService:
    def __init__(self):
        self.portfolio = {}

    def __add_buy_trade(self, trade: Trade):
        if trade.symbol not in self.portfolio:
            self.portfolio[trade.symbol] = {
                "quantity": trade.quantity,
                "average_price": trade.price
            }
        else:
            current_quantity = self.portfolio[trade.symbol]["quantity"]
            current_avg_price = self.portfolio[trade.symbol]["average_price"]
            
            total_cost = (current_avg_price * current_quantity) + (trade.price * trade.quantity)
            new_quantity = current_quantity + trade.quantity
            
            self.portfolio[trade.symbol]["quantity"] = new_quantity
            self.portfolio[trade.symbol]["average_price"] = total_cost / new_quantity

    def __add_sell_trade(self, trade: Trade):
        if trade.symbol not in self.portfolio:
            raise ValueError(f"Cannot sell {trade.symbol}: No holdings found in portfolio")
        
        current_quantity = self.portfolio[trade.symbol]["quantity"]
        
        if trade.quantity > current_quantity:
            raise ValueError(f"Cannot sell {trade.quantity} {trade.symbol}: Only {current_quantity} available")
        
        new_quantity = current_quantity - trade.quantity
        
        if new_quantity == 0:
            del self.portfolio[trade.symbol]
        else:
            self.portfolio[trade.symbol]["quantity"] = new_quantity

    def add_trade(self, trade: Trade):
        print(f"Adding trade: {trade}")
        
        if trade.side.lower() == "buy":
            self.__add_buy_trade(trade)
        elif trade.side.lower() == "sell":
            self.__add_sell_trade(trade)
        else:
            raise ValueError(f"Invalid trade side: {trade.side}. Must be 'buy' or 'sell'")

    def get_coin_data(self, symbol: str) -> Dict:
        if symbol not in self.portfolio:
            raise ValueError(f"Coin {symbol} not found in portfolio")
        return self.portfolio[symbol]
    
    def get_holdings(self) -> Dict:
        return self.portfolio