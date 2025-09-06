import pytest
import json


class TestTradeEndpoints:

    def test_add_trade_success(self, client):
        trade_data = {
            "symbol": "BTC",
            "side": "buy",
            "price": 50000.0,
            "quantity": 0.1
        }
        
        response = client.post('/trades', 
                             data=json.dumps(trade_data),
                             content_type='application/json')
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['message'] == 'Trade added successfully'
        assert data['trade']['symbol'] == 'BTC'
        assert data['trade']['side'] == 'buy'
        assert data['trade']['price'] == 50000.0
        assert data['trade']['quantity'] == 0.1
        assert 'id' in data['trade']
        assert 'timestamp' in data['trade']

    def test_add_trade_missing_fields(self, client):
        trade_data = {
            "symbol": "BTC",
            "side": "buy"
        }
        
        response = client.post('/trades',
                             data=json.dumps(trade_data),
                             content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_add_trade_invalid_side(self, client):
        trade_data = {
            "symbol": "BTC",
            "side": "invalid",
            "price": 50000.0,
            "quantity": 0.1
        }
        
        response = client.post('/trades',
                             data=json.dumps(trade_data),
                             content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_add_trade_negative_price(self, client):
        trade_data = {
            "symbol": "BTC",
            "side": "buy",
            "price": -1000.0,
            "quantity": 0.1
        }
        
        response = client.post('/trades',
                             data=json.dumps(trade_data),
                             content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_add_trade_negative_quantity(self, client):
        trade_data = {
            "symbol": "BTC",
            "side": "buy",
            "price": 50000.0,
            "quantity": -0.1
        }
        
        response = client.post('/trades',
                             data=json.dumps(trade_data),
                             content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_add_trade_non_json(self, client):
        response = client.post('/trades',
                             data="invalid data",
                             content_type='text/plain')
        
        assert response.status_code == 400

    def test_get_trades_empty(self, client):
        response = client.get('/trades')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['trades'] == []
        assert data['count'] == 0

    def test_get_trades_with_data(self, client, sample_trades):
        for trade in sample_trades:
            client.post('/trades',
                       data=json.dumps(trade),
                       content_type='application/json')
        
        response = client.get('/trades')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data['trades']) == len(sample_trades)
        assert data['count'] == len(sample_trades)
        for i, trade in enumerate(data['trades']):
            assert trade['symbol'] == sample_trades[i]['symbol']
            assert trade['side'] == sample_trades[i]['side']
            assert trade['price'] == sample_trades[i]['price']
            assert trade['quantity'] == sample_trades[i]['quantity']

    def test_add_multiple_trades(self, client):
        trades = [
            {"symbol": "BTC", "side": "buy", "price": 50000.0, "quantity": 0.1},
            {"symbol": "ETH", "side": "buy", "price": 3000.0, "quantity": 1.0},
            {"symbol": "BTC", "side": "sell", "price": 52000.0, "quantity": 0.05}
        ]
        
        for trade in trades:
            response = client.post('/trades',
                                 data=json.dumps(trade),
                                 content_type='application/json')
            assert response.status_code == 201
        response = client.get('/trades')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data['trades']) == 3
        assert data['count'] == 3
