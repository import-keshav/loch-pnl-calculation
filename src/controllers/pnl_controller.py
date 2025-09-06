from flask import jsonify, request
from src.managers.pnl_manager import PnLManager


class PnLController:
    def __init__(self, pnl_manager: PnLManager):
        self.pnl_manager = pnl_manager

    def register_routes(self, app):
        @app.route('/pnl', methods=['GET'])
        def get_pnl_endpoint():
            try:
                pnl_summary = self.pnl_manager.get_pnl()
                return jsonify(pnl_summary.to_dict()), 200
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @app.route('/pnl/<symbol>', methods=['GET'])
        def get_pnl_for_symbol_endpoint(symbol):
            try:
                pnl_data = self.pnl_manager.get_pnl_for_symbol(symbol.upper())
                return jsonify(pnl_data.to_dict()), 200
            except ValueError as e:
                return jsonify({"error": str(e)}), 404
            except Exception as e:
                return jsonify({"error": str(e)}), 500
