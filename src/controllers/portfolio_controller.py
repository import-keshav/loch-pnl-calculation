from flask import jsonify
from src.managers.portfolio_manager import PortfolioManager


class PortfolioController:
    def __init__(self, portfolio_manager: PortfolioManager):
        self.portfolio_manager = portfolio_manager

    def register_routes(self, app):
        @app.route('/portfolio', methods=['GET'])
        def get_portfolio_endpoint():
            try:
                portfolio_list = self.portfolio_manager.get_portfolio()
                return jsonify({
                    "portfolio": portfolio_list,
                    "count": len(portfolio_list)
                }), 200
            except Exception as e:
                return jsonify({"error": str(e)}), 500
