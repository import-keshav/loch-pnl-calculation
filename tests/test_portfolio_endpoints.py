import pytest
import json


class TestPortfolioEndpoints:
    """Test cases for portfolio endpoints"""

    def test_get_portfolio_empty(self, client):
        """Test getting portfolio when no trades exist"""
        response = client.get('/portfolio')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['portfolio'] == []
        assert data['count'] == 0

    def test_get_portfolio_single_buy_trade(self, client):
        """Test portfolio after single buy trade"""
        trade_data = {
            "symbol": "BTC",
            "side": "buy",
            "price": 50000.0,
            "quantity": 0.1
        }
        
        client.post('/trades',
                   data=json.dumps(trade_data),
                   content_type='application/json')
        
        response = client.get('/portfolio')
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert len(data['portfolio']) == 1
        assert data['count'] == 1
        
        btc_holding = data['portfolio'][0]
        assert btc_holding['symbol'] == 'BTC'
        assert btc_holding['quantity'] == 0.1
        assert btc_holding['average_price'] == 50000.0

    def test_get_portfolio_multiple_buy_trades_same_symbol(self, client):
        """Test portfolio with multiple buy trades for same symbol"""
        trades = [
            {"symbol": "BTC", "side": "buy", "price": 50000.0, "quantity": 0.1},
            {"symbol": "BTC", "side": "buy", "price": 52000.0, "quantity": 0.1}
        ]
        
        for trade in trades:
            client.post('/trades',
                       data=json.dumps(trade),
                       content_type='application/json')
        
        response = client.get('/portfolio')
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert len(data['portfolio']) == 1
        assert data['count'] == 1
        
        btc_holding = data['portfolio'][0]
        assert btc_holding['symbol'] == 'BTC'
        assert btc_holding['quantity'] == 0.2
        assert btc_holding['average_price'] == 51000.0

    def test_get_portfolio_multiple_symbols(self, client):
        """Test portfolio with multiple symbols"""
        trades = [
            {"symbol": "BTC", "side": "buy", "price": 50000.0, "quantity": 0.1},
            {"symbol": "ETH", "side": "buy", "price": 3000.0, "quantity": 2.0},
            {"symbol": "SOL", "side": "buy", "price": 100.0, "quantity": 10.0}
        ]
        
        for trade in trades:
            client.post('/trades',
                       data=json.dumps(trade),
                       content_type='application/json')
        
        response = client.get('/portfolio')
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert len(data['portfolio']) == 3
        assert data['count'] == 3
        
        symbols = {holding['symbol']: holding for holding in data['portfolio']}
        
        assert symbols['BTC']['quantity'] == 0.1
        assert symbols['BTC']['average_price'] == 50000.0
        
        assert symbols['ETH']['quantity'] == 2.0
        assert symbols['ETH']['average_price'] == 3000.0
        
        assert symbols['SOL']['quantity'] == 10.0
        assert symbols['SOL']['average_price'] == 100.0

    def test_get_portfolio_with_sell_trade(self, client):
        """Test portfolio after buy and sell trades"""
        trades = [
            {"symbol": "BTC", "side": "buy", "price": 50000.0, "quantity": 0.2},
            {"symbol": "BTC", "side": "sell", "price": 55000.0, "quantity": 0.1}
        ]
        
        for trade in trades:
            client.post('/trades',
                       data=json.dumps(trade),
                       content_type='application/json')
        
        response = client.get('/portfolio')
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert len(data['portfolio']) == 1
        assert data['count'] == 1
        
        btc_holding = data['portfolio'][0]
        assert btc_holding['symbol'] == 'BTC'
        assert btc_holding['quantity'] == 0.1
        assert btc_holding['average_price'] == 50000.0

    def test_get_portfolio_sell_all_holdings(self, client):
        """Test portfolio after selling all holdings"""
        trades = [
            {"symbol": "BTC", "side": "buy", "price": 50000.0, "quantity": 0.1},
            {"symbol": "BTC", "side": "sell", "price": 55000.0, "quantity": 0.1}
        ]
        
        for trade in trades:
            client.post('/trades',
                       data=json.dumps(trade),
                       content_type='application/json')
        
        response = client.get('/portfolio')
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert len(data['portfolio']) == 0
        assert data['count'] == 0

    def test_get_portfolio_complex_scenario(self, client):
        """Test portfolio with complex buy/sell scenario"""
        trades = [
            {"symbol": "BTC", "side": "buy", "price": 45000.0, "quantity": 0.2},
            {"symbol": "BTC", "side": "buy", "price": 55000.0, "quantity": 0.1},
            {"symbol": "ETH", "side": "buy", "price": 2800.0, "quantity": 3.0},
            {"symbol": "BTC", "side": "sell", "price": 60000.0, "quantity": 0.15},
            {"symbol": "ETH", "side": "buy", "price": 3200.0, "quantity": 1.0}
        ]
        
        for trade in trades:
            client.post('/trades',
                       data=json.dumps(trade),
                       content_type='application/json')
        
        response = client.get('/portfolio')
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert len(data['portfolio']) == 2
        assert data['count'] == 2
        
        symbols = {holding['symbol']: holding for holding in data['portfolio']}
        
        assert abs(symbols['BTC']['quantity'] - 0.15) < 0.0001
        assert abs(symbols['BTC']['average_price'] - 48333.33) < 0.01
        
        assert symbols['ETH']['quantity'] == 4.0
        assert symbols['ETH']['average_price'] == 2900.0
