import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from flask import Flask
from src.services.portfolio_service import PortfolioService
from src.services.price_service import PriceService
from src.services.trade_service import TradeService
from src.managers.trade_manager import TradeManager
from src.managers.portfolio_manager import PortfolioManager
from src.managers.pnl_manager import PnLManager
from src.controllers.trade_controller import TradeController
from src.controllers.portfolio_controller import PortfolioController
from src.controllers.pnl_controller import PnLController


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    
    portfolio_service = PortfolioService()
    price_service = PriceService()
    trade_service = TradeService()
    
    trade_manager = TradeManager(trade_service, portfolio_service)
    portfolio_manager = PortfolioManager(portfolio_service)
    pnl_manager = PnLManager(portfolio_service, price_service, trade_service)
    
    trade_controller = TradeController(trade_manager)
    portfolio_controller = PortfolioController(portfolio_manager)
    pnl_controller = PnLController(pnl_manager)
    
    trade_controller.register_routes(app)
    portfolio_controller.register_routes(app)
    pnl_controller.register_routes(app)
    
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def sample_trades():
    return [
        {
            "symbol": "BTC",
            "side": "buy",
            "price": 50000.0,
            "quantity": 0.1
        },
        {
            "symbol": "BTC", 
            "side": "buy",
            "price": 52000.0,
            "quantity": 0.05
        },
        {
            "symbol": "ETH",
            "side": "buy", 
            "price": 3000.0,
            "quantity": 2.0
        },
        {
            "symbol": "BTC",
            "side": "sell",
            "price": 55000.0,
            "quantity": 0.02
        }
    ]
