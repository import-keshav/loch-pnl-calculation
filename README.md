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
- **Responsibilities**:
  - Route registration with Flask
  - Request validation using Marshmallow
  - Response formatting (JSON)
  - Error handling and HTTP status codes
- **Files**:
  - `trade_controller.py` - Manages trade-related endpoints
  - `portfolio_controller.py` - Manages portfolio-related endpoints
  - `pnl_controller.py` - Manages PnL calculation endpoints

### 2. **Managers Layer** (`src/managers/`)
- **Purpose**: Orchestrate business logic between multiple services
- **Responsibilities**:
  - Coordinate operations across different services
  - Handle complex business workflows
  - Manage transactions and data consistency
- **Files**:
  - `trade_manager.py` - Orchestrates trade processing
  - `portfolio_manager.py` - Manages portfolio operations
  - `pnl_manager.py` - Handles PnL calculations

### 3. **Services Layer** (`src/services/`)
- **Purpose**: Implement core business logic
- **Responsibilities**:
  - Data manipulation and storage
  - Business rule implementation
  - External API integrations
- **Files**:
  - `trade_service.py` - Trade data management
  - `portfolio_service.py` - Portfolio calculations and updates
  - `price_service.py` - Price data management
  - `pnl_service.py` - PnL calculation logic

### 4. **Models Layer** (`src/models/`)
- **Purpose**: Define data entities and structures
- **Responsibilities**:
  - Data validation
  - Entity relationships
  - Business object representation
- **Files**:
  - `trade.py` - Trade entity definition
  - `portfolio.py` - Portfolio entity definition

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
1. **Trade Creation**: `POST /trades` → Controller → Manager → Service → Model
2. **Portfolio Update**: Trade Service → Portfolio Service (handles buy/sell logic)
3. **Portfolio Retrieval**: `GET /portfolio` → Controller → Manager → Service
4. **PnL Calculation**: `GET /pnl` → Controller → Manager → Services (Portfolio + Price + Trade)

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

### Production Deployment
```bash
# Using Gunicorn (recommended for production)
gunicorn main:app --bind 0.0.0.0:8000
```

## API Endpoints

### 1. Add Trade
**Endpoint**: `POST /trades`

**Description**: Record a new trade transaction

**Request Body**:
```json
{
    "symbol": "BTC",
    "side": "buy",
    "price": 50000.0,
    "quantity": 0.1
}
```

**Response** (201 Created):
```json
{
    "message": "Trade added successfully",
    "trade": {
        "id": "trade_20241201_143022_123456",
        "symbol": "BTC",
        "side": "buy",
        "price": 50000.0,
        "quantity": 0.1,
        "timestamp": "2024-12-01T14:30:22.123456"
    }
}
```

**cURL Example**:
```bash
curl -X POST http://127.0.0.1:8000/trades \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "BTC",
    "side": "buy",
    "price": 50000.0,
    "quantity": 0.1
  }'
```

### 2. Get All Trades
**Endpoint**: `GET /trades`

**Description**: Retrieve all recorded trades

**Response** (200 OK):
```json
{
    "trades": [
        {
            "id": "trade_20241201_143022_123456",
            "symbol": "BTC",
            "side": "buy",
            "price": 50000.0,
            "quantity": 0.1,
            "timestamp": "2024-12-01T14:30:22.123456"
        }
    ],
    "count": 1
}
```

**cURL Example**:
```bash
curl -X GET http://127.0.0.1:8000/trades
```

### 3. Get Portfolio Holdings
**Endpoint**: `GET /portfolio`

**Description**: Retrieve current portfolio holdings with average prices

**Response** (200 OK):
```json
{
    "portfolio": [
        {
            "symbol": "BTC",
            "quantity": 0.15,
            "average_price": 50666.67
        },
        {
            "symbol": "ETH",
            "quantity": 2.0,
            "average_price": 3000.0
        }
    ],
    "count": 2
}
```

**cURL Example**:
```bash
curl -X GET http://127.0.0.1:8000/portfolio
```

### 4. Get Complete PnL (Unrealized + Realized)
**Endpoint**: `GET /pnl`

**Description**: Calculate and retrieve complete profit/loss including both unrealized and realized PnL for all portfolio holdings

**Response** (200 OK):
```json
{
    "pnl": [
        {
            "symbol": "BTC",
            "quantity": 0.15,
            "average_price": 50666.67,
            "current_price": 55000.0,
            "unrealized_pnl": 650.0,
            "realized_pnl": 1200.0,
            "total_pnl": 1850.0
        },
        {
            "symbol": "ETH",
            "quantity": 2.0,
            "average_price": 3000.0,
            "current_price": 3200.0,
            "unrealized_pnl": 400.0,
            "realized_pnl": 0.0,
            "total_pnl": 400.0
        }
    ],
    "total_unrealized_pnl": 1050.0,
    "total_realized_pnl": 1200.0,
    "total_pnl": 2250.0,
    "count": 2
}
```

**cURL Example**:
```bash
curl -X GET http://127.0.0.1:8000/pnl
```

### 5. Get PnL for Single Symbol
**Endpoint**: `GET /pnl/{symbol}`

**Description**: Get PnL information for a specific cryptocurrency

**Response** (200 OK):
```json
{
    "symbol": "BTC",
    "quantity": 0.15,
    "average_price": 50666.67,
    "current_price": 55000.0,
    "unrealized_pnl": 650.0,
    "realized_pnl": 1200.0,
    "total_pnl": 1850.0
}
```

**cURL Example**:
```bash
curl -X GET http://127.0.0.1:8000/pnl/BTC
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

## Dependencies

- Flask 2.3.3 - Web framework for API endpoints
- marshmallow 3.20.1 - Request/response validation and serialization
- pytest 7.4.3 - Testing framework
- pytest-flask 1.3.0 - Flask-specific testing utilities
- ruff 0.1.6 - Python linter and formatter
- gunicorn 21.2.0 - Production WSGI server
- python-dotenv 1.0.0 - Environment variable management
- python-dateutil 2.8.2 - Date/time utilities

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