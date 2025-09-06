import pytest
import json


class TestPnLEndpoints:

    def test_get_pnl_empty_portfolio(self, client):
        response = client.get('/pnl')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['pnl'] == []
        assert data['total_unrealized_pnl'] == 0.0
        assert data['total_realized_pnl'] == 0.0
        assert data['total_pnl'] == 0.0
        assert data['count'] == 0

    def test_get_pnl_single_symbol_no_sells(self, client):
        trade_data = {
            "symbol": "BTC",
            "side": "buy",
            "price": 50000.0,
            "quantity": 0.1
        }
        
        client.post('/trades',
                   data=json.dumps(trade_data),
                   content_type='application/json')
        
        response = client.get('/pnl')
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert len(data['pnl']) == 1
        assert data['count'] == 1
        
        btc_pnl = data['pnl'][0]
        assert btc_pnl['symbol'] == 'BTC'
        assert btc_pnl['quantity'] == 0.1
        assert btc_pnl['average_price'] == 50000.0
        assert btc_pnl['current_price'] == 10000.0
        assert btc_pnl['unrealized_pnl'] == -4000.0
        assert btc_pnl['realized_pnl'] == 0.0
        assert btc_pnl['total_pnl'] == -4000.0

    def test_get_pnl_with_realized_gains(self, client):
        trades = [
            {"symbol": "BTC", "side": "buy", "price": 45000.0, "quantity": 0.2},
            {"symbol": "BTC", "side": "sell", "price": 50000.0, "quantity": 0.1}
        ]
        
        for trade in trades:
            client.post('/trades',
                       data=json.dumps(trade),
                       content_type='application/json')
        
        response = client.get('/pnl')
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert len(data['pnl']) == 1
        btc_pnl = data['pnl'][0]
        
        assert btc_pnl['symbol'] == 'BTC'
        assert btc_pnl['quantity'] == 0.1
        assert btc_pnl['average_price'] == 45000.0
        assert btc_pnl['current_price'] == 10000.0
        assert btc_pnl['unrealized_pnl'] == -3500.0
        assert btc_pnl['realized_pnl'] == 500.0
        assert btc_pnl['total_pnl'] == -3000.0

    def test_get_pnl_multiple_symbols(self, client):
        trades = [
            {"symbol": "BTC", "side": "buy", "price": 50000.0, "quantity": 0.1},
            {"symbol": "ETH", "side": "buy", "price": 3000.0, "quantity": 1.0},
            {"symbol": "BTC", "side": "sell", "price": 55000.0, "quantity": 0.05}
        ]
        
        for trade in trades:
            client.post('/trades',
                       data=json.dumps(trade),
                       content_type='application/json')
        
        response = client.get('/pnl')
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert len(data['pnl']) == 2
        assert data['count'] == 2
        
        symbols = {pnl['symbol']: pnl for pnl in data['pnl']}
        
        btc_pnl = symbols['BTC']
        assert btc_pnl['quantity'] == 0.05
        assert btc_pnl['average_price'] == 50000.0
        assert btc_pnl['current_price'] == 10000.0
        assert btc_pnl['unrealized_pnl'] == -2000.0
        assert btc_pnl['realized_pnl'] == 250.0
        assert btc_pnl['total_pnl'] == -1750.0
        
        eth_pnl = symbols['ETH']
        assert eth_pnl['quantity'] == 1.0
        assert eth_pnl['average_price'] == 3000.0
        assert eth_pnl['current_price'] == 2000.0
        assert eth_pnl['unrealized_pnl'] == -1000.0
        assert eth_pnl['realized_pnl'] == 0.0
        assert eth_pnl['total_pnl'] == -1000.0
        
        assert data['total_unrealized_pnl'] == -3000.0
        assert data['total_realized_pnl'] == 250.0
        assert data['total_pnl'] == -2750.0

    def test_get_pnl_for_symbol_success(self, client):
        trades = [
            {"symbol": "BTC", "side": "buy", "price": 45000.0, "quantity": 0.2},
            {"symbol": "ETH", "side": "buy", "price": 3000.0, "quantity": 1.0},
            {"symbol": "BTC", "side": "sell", "price": 50000.0, "quantity": 0.1}
        ]
        
        for trade in trades:
            client.post('/trades',
                       data=json.dumps(trade),
                       content_type='application/json')
        
        response = client.get('/pnl/BTC')
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['symbol'] == 'BTC'
        assert data['quantity'] == 0.1
        assert data['average_price'] == 45000.0
        assert data['current_price'] == 10000.0
        assert data['unrealized_pnl'] == -3500.0
        assert data['realized_pnl'] == 500.0
        assert data['total_pnl'] == -3000.0

    def test_get_pnl_for_symbol_not_found(self, client):
        response = client.get('/pnl/NONEXISTENT')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data

    def test_get_pnl_for_symbol_case_insensitive(self, client):
        trade_data = {
            "symbol": "BTC",
            "side": "buy",
            "price": 50000.0,
            "quantity": 0.1
        }
        
        client.post('/trades',
                   data=json.dumps(trade_data),
                   content_type='application/json')
        
        response = client.get('/pnl/btc')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['symbol'] == 'BTC'

    def test_get_pnl_complex_scenario(self, client):
        trades = [
            {"symbol": "BTC", "side": "buy", "price": 40000.0, "quantity": 0.3},
            {"symbol": "BTC", "side": "buy", "price": 50000.0, "quantity": 0.2},
            {"symbol": "ETH", "side": "buy", "price": 2500.0, "quantity": 2.0},
            {"symbol": "ETH", "side": "buy", "price": 3500.0, "quantity": 1.0},
            {"symbol": "BTC", "side": "sell", "price": 55000.0, "quantity": 0.2},
            {"symbol": "ETH", "side": "sell", "price": 3000.0, "quantity": 0.5}
        ]
        
        for trade in trades:
            client.post('/trades',
                       data=json.dumps(trade),
                       content_type='application/json')
        
        response = client.get('/pnl')
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert len(data['pnl']) == 2
        symbols = {pnl['symbol']: pnl for pnl in data['pnl']}
        
        btc_pnl = symbols['BTC']
        assert btc_pnl['quantity'] == 0.3
        assert btc_pnl['average_price'] == 44000.0
        assert btc_pnl['realized_pnl'] == 2200.0
        assert btc_pnl['unrealized_pnl'] == -10200.0
        assert btc_pnl['total_pnl'] == -8000.0
        
        eth_pnl = symbols['ETH']
        assert eth_pnl['quantity'] == 2.5
        assert abs(eth_pnl['average_price'] - 2833.33) < 0.01
        assert abs(eth_pnl['realized_pnl'] - 83.33) < 0.01
        assert abs(eth_pnl['unrealized_pnl'] - (-2083.33)) < 0.01