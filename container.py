from src.models.trade import Trade

from src.services.portfolio_service import PortfolioService
from src.services.price_service import PriceService
from src.services.trade_service import TradeService

from src.managers.trade_manager import TradeManager
from src.managers.portfolio_manager import PortfolioManager
from src.managers.pnl_manager import PnLManager

from src.controllers.trade_controller import TradeController
from src.controllers.portfolio_controller import PortfolioController
from src.controllers.pnl_controller import PnLController


portfolio_service = PortfolioService()
price_service = PriceService()
trade_service = TradeService()

trade_manager = TradeManager(trade_service, portfolio_service)
portfolio_manager = PortfolioManager(portfolio_service)
pnl_manager = PnLManager(portfolio_service, price_service, trade_service)

trade_controller = TradeController(trade_manager)
portfolio_controller = PortfolioController(portfolio_manager)
pnl_controller = PnLController(pnl_manager)
