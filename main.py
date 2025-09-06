from flask import Flask
from container import trade_controller, portfolio_controller, pnl_controller

app = Flask(__name__)

trade_controller.register_routes(app)
portfolio_controller.register_routes(app)
pnl_controller.register_routes(app)

if __name__ == "__main__":
    app.run(debug=True, port=8000)