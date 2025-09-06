from src.services.portfolio_service import PortfolioService
from src.services.price_service import PriceService
from src.services.trade_service import TradeService
from src.dtos.pnl_dto import (
    UnrealizedPnLDto, 
    RealizedPnLDto, 
    CombinedPnLDto, 
    PnLSummaryDto
)


class PnLManager:
    def __init__(self, portfolio_service: PortfolioService, price_service: PriceService, trade_service: TradeService):
        self.portfolio_service = portfolio_service
        self.price_service = price_service
        self.trade_service = trade_service

    def _calculate_unrealized_pnl_for_holding(self, symbol: str, quantity: float, average_price: float, current_price: float) -> UnrealizedPnLDto:
        unrealized_pnl = (current_price - average_price) * quantity
        
        return UnrealizedPnLDto(
            symbol=symbol,
            quantity=quantity,
            average_price=average_price,
            current_price=current_price,
            unrealized_pnl=round(unrealized_pnl, 2)
        )

    def _calculate_realized_pnl_for_symbol(self, symbol: str) -> RealizedPnLDto:
        all_trades = self.trade_service.get_trades_by_symbol_and_side(symbol)
        
        if not all_trades:
            return RealizedPnLDto(
                symbol=symbol,
                total_realized_pnl=0.0,
                note="No trades found for this symbol"
            )
        
        sorted_trades = sorted(all_trades, key=lambda t: t.timestamp)
        
        total_realized_pnl = 0
        running_quantity = 0
        running_total_cost = 0
        
        for trade in sorted_trades:
            if trade.side.lower() == "buy":
                running_total_cost += trade.price * trade.quantity
                running_quantity += trade.quantity
                
            elif trade.side.lower() == "sell":
                if running_quantity > 0:
                    current_avg_price = running_total_cost / running_quantity
                    trade_pnl = (trade.price - current_avg_price) * trade.quantity
                    total_realized_pnl += trade_pnl
                    
                    running_quantity -= trade.quantity
                    if running_quantity > 0:
                        running_total_cost = current_avg_price * running_quantity
                    else:
                        running_total_cost = 0
        
        return RealizedPnLDto(
            symbol=symbol,
            total_realized_pnl=round(total_realized_pnl, 2)
        )

    def get_pnl(self) -> PnLSummaryDto:
        holdings = self.portfolio_service.get_holdings()
        pnl_data = []
        total_unrealized_pnl = 0
        total_realized_pnl = 0

        for symbol, data in holdings.items():
            current_price = self.price_service.get_price(symbol)
            
            unrealized_result = self._calculate_unrealized_pnl_for_holding(
                symbol=symbol,
                quantity=data["quantity"],
                average_price=data["average_price"],
                current_price=current_price
            )
            
            realized_result = self._calculate_realized_pnl_for_symbol(symbol)
            
            combined_pnl = CombinedPnLDto(
                symbol=unrealized_result.symbol,
                quantity=unrealized_result.quantity,
                average_price=unrealized_result.average_price,
                current_price=unrealized_result.current_price,
                unrealized_pnl=unrealized_result.unrealized_pnl,
                realized_pnl=realized_result.total_realized_pnl,
                total_pnl=round(unrealized_result.unrealized_pnl + realized_result.total_realized_pnl, 2)
            )
            
            total_unrealized_pnl += unrealized_result.unrealized_pnl
            total_realized_pnl += realized_result.total_realized_pnl
            pnl_data.append(combined_pnl)

        return PnLSummaryDto(
            pnl=pnl_data,
            total_unrealized_pnl=round(total_unrealized_pnl, 2),
            total_realized_pnl=round(total_realized_pnl, 2),
            total_pnl=round(total_unrealized_pnl + total_realized_pnl, 2),
            count=len(pnl_data)
        )

    def get_pnl_for_symbol(self, symbol: str) -> CombinedPnLDto:
        try:
            coin_data = self.portfolio_service.get_coin_data(symbol)
            current_price = self.price_service.get_price(symbol)
            
            unrealized_result = self._calculate_unrealized_pnl_for_holding(
                symbol=symbol,
                quantity=coin_data["quantity"],
                average_price=coin_data["average_price"],
                current_price=current_price
            )
            
            realized_result = self._calculate_realized_pnl_for_symbol(symbol)
            
            return CombinedPnLDto(
                symbol=unrealized_result.symbol,
                quantity=unrealized_result.quantity,
                average_price=unrealized_result.average_price,
                current_price=unrealized_result.current_price,
                unrealized_pnl=unrealized_result.unrealized_pnl,
                realized_pnl=realized_result.total_realized_pnl,
                total_pnl=round(unrealized_result.unrealized_pnl + realized_result.total_realized_pnl, 2)
            )
        except ValueError as e:
            raise ValueError(f"Cannot calculate PnL: {str(e)}")