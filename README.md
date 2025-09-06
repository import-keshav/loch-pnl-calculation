# Loch PnL Calculation System

A Portfolio & Profit/Loss (PnL) calculation system built with Flask, following clean architecture principles.

## Code Architecture

This project follows a **layered architecture** with clear separation of concerns, making it maintainable, testable, and scalable.

### Architecture Layers

```
┌─────────────────────────────────────────┐
│              Controllers                │  ← HTTP Request/Response Layer
├─────────────────────────────────────────┤
│               Managers                  │  ← Business Logic Orchestration
├─────────────────────────────────────────┤
│               Services                  │  ← Core Business Logic
├─────────────────────────────────────────┤
│                Models                   │  ← Data Entities
└─────────────────────────────────────────┘
```

### 1. **Controllers Layer** (`src/controllers/`)
- **Purpose**: Handle HTTP requests and responses

### 2. **Managers Layer** (`src/managers/`)
- **Purpose**: Orchestrate business logic between multiple services

### 3. **Services Layer** (`src/services/`)
- **Purpose**: Implement core business logic

### 4. **Models Layer** (`src/models/`)
- **Purpose**: Define data entities and structures

## Entities and Data Flow

### Trade Entity
```python
Trade {
    trade_id: str      # Unique identifier
    symbol: str        # Cryptocurrency symbol (BTC, ETH, etc.)
    side: str          # "buy" or "sell"
    price: float       # Trade execution price
    quantity: float    # Amount traded
    timestamp: str     # ISO format timestamp
}
```

### Portfolio Entity
```python
Portfolio {
    symbol: str           # Cryptocurrency symbol
    quantity: float       # Current holdings (after buy/sell trades)
    average_price: float  # Weighted average purchase price
}
```

### PnL Entity (DTO)
```python
CombinedPnLDto {
    symbol: str              # Cryptocurrency symbol
    quantity: float          # Current holdings quantity
    average_price: float     # Weighted average purchase price
    current_price: float     # Current market price
    unrealized_pnl: float    # Unrealized profit/loss
    realized_pnl: float      # Realized profit/loss from sells
    total_pnl: float         # Combined unrealized + realized PnL
}
```

### Data Flow Example
**PnL Calculation**: `GET /pnl` → Controller → Manager → Services (Portfolio + Price + Trade)

## Getting Started

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd loch-pnl-calculation
   ```

2. **Create and activate virtual environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # On macOS/Linux:
   source venv/bin/activate
   
   # On Windows:
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

   The server will start on `http://127.0.0.1:8000`


## API Endpoints

### 1. Add Trade
```bash
curl -X POST http://127.0.0.1:8000/trades \
  -H "Content-Type: application/json" \
  -d '{"symbol": "BTC", "side": "buy", "price": 50000.0, "quantity": 0.1}'
```

### 2. Get Portfolio
```bash
curl -X GET http://127.0.0.1:8000/portfolio
```

### 3. Get PnL
```bash
curl -X GET http://127.0.0.1:8000/pnl
```

## Testing the API

### Complete Test Flow

#### Step 1: Add Buy Trades
```bash
# Add initial BTC buy trade
curl -X POST http://127.0.0.1:8000/trades \
  -H "Content-Type: application/json" \
  -d '{"symbol": "BTC", "side": "buy", "price": 50000.0, "quantity": 0.2}'

# Add another BTC buy trade (tests weighted average price)
curl -X POST http://127.0.0.1:8000/trades \
  -H "Content-Type: application/json" \
  -d '{"symbol": "BTC", "side": "buy", "price": 52000.0, "quantity": 0.1}'

# Add ETH buy trade
curl -X POST http://127.0.0.1:8000/trades \
  -H "Content-Type: application/json" \
  -d '{"symbol": "ETH", "side": "buy", "price": 3000.0, "quantity": 2.0}'

# Add another ETH buy trade
curl -X POST http://127.0.0.1:8000/trades \
  -H "Content-Type: application/json" \
  -d '{"symbol": "ETH", "side": "buy", "price": 3200.0, "quantity": 1.0}'
```

#### Step 2: Add Sell Trades
```bash
# Sell some BTC (generates realized PnL)
curl -X POST http://127.0.0.1:8000/trades \
  -H "Content-Type: application/json" \
  -d '{"symbol": "BTC", "side": "sell", "price": 53000.0, "quantity": 0.05}'

# Sell more BTC at different price
curl -X POST http://127.0.0.1:8000/trades \
  -H "Content-Type: application/json" \
  -d '{"symbol": "BTC", "side": "sell", "price": 55000.0, "quantity": 0.1}'

# Sell some ETH
curl -X POST http://127.0.0.1:8000/trades \
  -H "Content-Type: application/json" \
  -d '{"symbol": "ETH", "side": "sell", "price": 3300.0, "quantity": 0.5}'
```

#### Step 3: View Results
```bash
# View all trades
curl -X GET http://127.0.0.1:8000/trades

# View portfolio holdings (current positions)
curl -X GET http://127.0.0.1:8000/portfolio

# View complete PnL (unrealized + realized for all holdings)
curl -X GET http://127.0.0.1:8000/pnl

# View detailed BTC PnL with individual realized trades
curl -X GET http://127.0.0.1:8000/pnl/BTC

# View detailed ETH PnL
curl -X GET http://127.0.0.1:8000/pnl/ETH
```

### Quick Test Commands

#### Basic Portfolio Test:
```bash
# Quick 3-step test
curl -X POST http://127.0.0.1:8000/trades -H "Content-Type: application/json" -d '{"symbol": "BTC", "side": "buy", "price": 50000.0, "quantity": 0.1}'
curl -X POST http://127.0.0.1:8000/trades -H "Content-Type: application/json" -d '{"symbol": "BTC", "side": "sell", "price": 52000.0, "quantity": 0.05}'
curl -X GET http://127.0.0.1:8000/pnl/BTC
```

#### Multi-Asset Test:
```bash
# Test multiple cryptocurrencies
curl -X POST http://127.0.0.1:8000/trades -H "Content-Type: application/json" -d '{"symbol": "BTC", "side": "buy", "price": 50000.0, "quantity": 0.1}'
curl -X POST http://127.0.0.1:8000/trades -H "Content-Type: application/json" -d '{"symbol": "ETH", "side": "buy", "price": 3000.0, "quantity": 1.0}'
curl -X POST http://127.0.0.1:8000/trades -H "Content-Type: application/json" -d '{"symbol": "SOL", "side": "buy", "price": 100.0, "quantity": 5.0}'
curl -X GET http://127.0.0.1:8000/pnl
```

#### Realized PnL Test:
```bash
# Test realized PnL calculation
curl -X POST http://127.0.0.1:8000/trades -H "Content-Type: application/json" -d '{"symbol": "BTC", "side": "buy", "price": 45000.0, "quantity": 0.2}'
curl -X POST http://127.0.0.1:8000/trades -H "Content-Type: application/json" -d '{"symbol": "BTC", "side": "sell", "price": 50000.0, "quantity": 0.1}'
curl -X GET http://127.0.0.1:8000/pnl/BTC
# Should show realized PnL of: (50000 - 45000) * 0.1 = 500.0
```

### Expected Results:
After running the complete test flow, you should see:
- Portfolio: Current holdings with weighted average prices
- Unrealized PnL: Profit/loss on current holdings vs current market prices
- Realized PnL: Profit/loss from completed sell trades vs average purchase price
- Total PnL: Combined unrealized + realized PnL

### Key Trading Logic:
- Buy Trades: Add to portfolio or update weighted average price
- Sell Trades: Reduce quantity, remove if zero, preserve average price
- PnL Calculation: Realized PnL = (sell_price - avg_price) × quantity
- Portfolio Updates: Automatic on every trade transaction

## Development

### Code Quality
```bash
# Run linter
ruff check .

# Format code
ruff format .
```

### Testing
```bash
# Install test dependencies
pip install -r requirements.txt

# Run all tests
pytest

# Run tests with coverage report
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_trade_endpoints.py

# Run tests with verbose output
pytest -v

# Run tests and stop on first failure
pytest -x
```

#### Test Structure
```
tests/
├── conftest.py              # Test configuration and fixtures
├── test_trade_endpoints.py  # Trade API endpoint tests
├── test_portfolio_endpoints.py  # Portfolio API endpoint tests
└── test_pnl_endpoints.py    # PnL API endpoint tests
```

#### Test Coverage
- **Trade Endpoints**: Add trades, get trades, validation, error handling
- **Portfolio Endpoints**: Portfolio calculations, buy/sell logic, weighted averages
- **PnL Endpoints**: Unrealized/realized PnL, complex scenarios, edge cases
- **Integration Tests**: Complete trading workflows and calculations

## Project Structure
```
loch-pnl-calculation/
├── main.py                 # Application entry point
├── container.py            # Dependency injection container
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── .gitignore             # Git ignore rules
├── src/                   # Source code
│   ├── controllers/       # HTTP request handlers
│   │   ├── trade_controller.py
│   │   ├── portfolio_controller.py
│   │   └── pnl_controller.py
│   ├── managers/          # Business logic orchestration
│   │   ├── trade_manager.py
│   │   ├── portfolio_manager.py
│   │   └── pnl_manager.py
│   ├── services/          # Core business logic
│   │   ├── trade_service.py
│   │   ├── portfolio_service.py
│   │   ├── price_service.py
│   │   └── pnl_service.py
│   ├── models/            # Data entities
│   │   ├── trade.py
│   │   └── portfolio.py
│   └── dtos/              # Data Transfer Objects
│       └── pnl_dto.py
└── tests/                 # Unit tests
    ├── conftest.py        # Test configuration
    ├── test_trade_endpoints.py
    ├── test_portfolio_endpoints.py
    └── test_pnl_endpoints.py
```