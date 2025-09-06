from flask import request, jsonify
from datetime import datetime
from marshmallow import Schema, fields, ValidationError
from src.managers.trade_manager import TradeManager
from src.models.trade import Trade


class TradeSchema(Schema):
    symbol = fields.Str(required=True)
    side = fields.Str(required=True, validate=lambda x: x.lower() in ['buy', 'sell'])
    price = fields.Float(required=True, validate=lambda x: x > 0)
    quantity = fields.Float(required=True, validate=lambda x: x > 0)


class TradeController:
    def __init__(self, trade_manager: TradeManager):
        self.trade_manager = trade_manager
        self.trade_schema = TradeSchema()

    def add_trade(self, trade: Trade):
        self.trade_manager.add_trade(trade)

    def register_routes(self, app):
        @app.route('/trades', methods=['POST'])
        def add_trade_endpoint():
            try:
                # Check if request has valid JSON
                try:
                    json_data = request.get_json(force=True)
                except Exception:
                    return jsonify({"error": "Invalid JSON data"}), 400
                
                if json_data is None:
                    return jsonify({"error": "Invalid JSON data"}), 400
                    
                data = self.trade_schema.load(json_data)
                trade_id = f"trade_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
                timestamp = datetime.now().isoformat()

                trade = Trade(
                    trade_id=trade_id,
                    symbol=data['symbol'].upper(),
                    side=data['side'].lower(),
                    price=data['price'],
                    quantity=data['quantity'],
                    timestamp=timestamp
                )
                
                self.add_trade(trade)
                
                return jsonify({
                    "message": "Trade added successfully",
                    "trade": {
                        "id": trade.trade_id,
                        "symbol": trade.symbol,
                        "side": trade.side,
                        "price": trade.price,
                        "quantity": trade.quantity,
                        "timestamp": trade.timestamp
                    }
                }), 201
                
            except ValidationError as e:
                return jsonify({"error": e.messages}), 400
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @app.route('/trades', methods=['GET'])
        def get_trades_endpoint():
            try:
                trades = self.trade_manager.trade_service.get_trades()
                return jsonify({
                    "trades": [
                        {
                            "id": trade.trade_id,
                            "symbol": trade.symbol,
                            "side": trade.side,
                            "price": trade.price,
                            "quantity": trade.quantity,
                            "timestamp": trade.timestamp
                        }
                        for trade in trades
                    ],
                    "count": len(trades)
                }), 200
            except Exception as e:
                return jsonify({"error": str(e)}), 500
