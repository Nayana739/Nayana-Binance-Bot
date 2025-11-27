# BINANCE BOT 

## Binance Futures Testnet Trading Bot  
A modular CLI-based trading bot designed for Binance USDT-M Futures Testnet.  
Supports Market Orders, Limit Orders, and optional advanced strategies such as Grid, TWAP, and OCO.  
Includes structured logging, input validation, dry-run mode, and reusable utilities.

##  Features

###  Core Features 
- Place **Market** orders  
- Place **Limit** orders  
- Validate user input (symbols, quantities)  
- Log all requests, responses, and errors into `bot.log`  
- Works with Binance **USDT-M Futures Testnet**  
- Supports **dry-run mode** for safe testing  
- Clean and modular architecture  

###  Optional Advanced Strategies
- **Grid Trading Strategy** 
- **TWAP (Time-Weighted Average Price)** 
- **Simulated OCO (Take-Profit + Stop-Loss)**

##  Project Structure

src/
│── utils.py                 # Logging, validation, Binance client, order wrapper
│── market_orders.py         # Market order execution
│── limit_orders.py          # Limit order execution
│── advanced/
│     ├── grid_strategy.py   # Grid strategy simulation
│     ├── oco.py             # OCO-like TP/SL strategy
│     └── twap.py              # TWAP execution
bot.log                      # Generated logs
requirements.txt
README.md

##  Installation

### 1. Clone the Repository
```bash
git clone <repo-url>
cd trader-bot
````

### 2. Create Virtual Environment

```bash
python -m venv env
source env/bin/activate   # Mac/Linux
env\Scripts\activate      # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Add API Keys

Add these to your system environment variables or `.env`:

```
BINANCE_API_KEY=your_key
BINANCE_API_SECRET=your_secret
USE_BINANCE_API=1
```

Set to `0` for dry-run mode:

```
USE_BINANCE_API=0
```

##  Usage (CLI)

###  Market Order

```bash
python src/market_orders.py BTCUSDT BUY 0.001
```

###  Limit Order

```bash
python src/limit_orders.py BTCUSDT SELL 0.001 62000
```

##  Optional Strategy Scripts

###  Grid Strategy

```bash
python src/advanced/grid_strategy.py BTCUSDT 60000 70000 5 0.001
```

###  OCO (Simulated TP + SL)

```bash
python src/advanced/oco.py BTCUSDT BUY 0.001 65000 58000
```

###  TWAP

```bash
python src/advanced/twap.py BTCUSDT BUY 0.01 5 60
```

##  Logging

All logs are saved automatically to:

```
bot.log
```

Including:

* Order requests
* Binance responses
* Dry-run simulations
* Errors
* Strategy steps (Grid, OCO, TWAP)

##  Utilities (utils.py)

The `utils.py` module handles:

* Structured logging
* Binance client creation
* Dry-run mode
* Order wrapper (`place_order`)
* Input validation (`validate_symbol`)
* Time utilities

This keeps the entire project modular and reusable.

## ✔ Requirements Satisfied (from project spec)

* Market + Limit order support
* Clean modular structure
* Logging to file
* CLI interface
* Testnet integration
* Error handling
* Optional advanced strategies
* Reusable helpers and order wrapper

##  License

This project is for educational and assignment purposes.
