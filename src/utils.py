import os
import logging
import json
import time
from datetime import datetime

# optional import; will be required only in live mode
try:
    from binance.client import Client
except Exception:
    Client = None

LOG_FILE = os.environ.get("BOT_LOG_FILE", "bot.log")
USE_BINANCE_API = os.environ.get("USE_BINANCE_API", "0") == "1"
API_KEY = os.environ.get("BINANCE_API_KEY", "")
API_SECRET = os.environ.get("BINANCE_API_SECRET", "")

# configure structured logging
logger = logging.getLogger("binance_bot")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | action=%(action)s details=%(details)s', "%Y-%m-%dT%H:%M:%S")

# file handler
fh = logging.FileHandler(LOG_FILE)
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)

# console handler
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)
logger.addHandler(ch)


def _log(level, action, details):
    extra = {"action": action, "details": json.dumps(details, default=str)}
    if level == "info":
        logger.info("", extra=extra)
    elif level == "debug":
        logger.debug("", extra=extra)
    elif level == "warning":
        logger.warning("", extra=extra)
    elif level == "error":
        logger.error("", extra=extra)


def create_binance_client():
    """
    Return a python-binance Client configured for futures (if available and enabled).
    """
    if not USE_BINANCE_API:
        _log("info", "create_binance_client", {"mode": "dry-run"})
        return None

    if Client is None:
        _log("error", "create_binance_client", {"error": "python-binance not installed"})
        raise RuntimeError("python-binance library not available. Install requirements.")

    client = Client(API_KEY, API_SECRET)
    _log("info", "create_binance_client", {"mode": "live"})
    return client


def iso_ts():
    return datetime.utcnow().isoformat(timespec="seconds") + "Z"


def validate_symbol(symbol: str):
    if not symbol or not symbol.endswith("USDT"):
        raise ValueError("Symbol should be a USDT pair, e.g., BTCUSDT")
    return symbol.upper()


def place_order(client, symbol: str, side: str, order_type: str, quantity: float, price: float = None, stop_price: float = None, reduce_only: bool = False, **kwargs):
    """
    Wrapper to place an order. In dry-run mode this just logs the order details and returns a simulated response.
    """
    payload = {
        "symbol": symbol,
        "side": side,
        "type": order_type,
        "quantity": quantity,
        "price": price,
        "stopPrice": stop_price,
        "reduceOnly": reduce_only,
        **kwargs
    }

    if not USE_BINANCE_API or client is None:
        _log("info", "place_order_simulation", {"mode": "dry-run", **payload})
        # simulated response
        return {"simulated": True, "payload": payload, "timestamp": iso_ts()}

    # live mode
    try:
        # map to futures endpoint (python-binance): client.futures_create_order(...)
        resp = client.futures_create_order(
            symbol=symbol,
            side=side,
            type=order_type,
            quantity=quantity,
            price=str(price) if price is not None else None,
            stopPrice=str(stop_price) if stop_price is not None else None,
            **{k: v for k, v in kwargs.items() if v is not None}
        )
        _log("info", "place_order_live", {"payload": payload, "response": resp})
        return resp
    except Exception as e:
        _log("error", "place_order_error", {"payload": payload, "error": str(e)})
        raise
