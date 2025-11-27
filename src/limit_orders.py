import argparse
from utils import create_binance_client, validate_symbol, place_order, _log

def main():
    parser = argparse.ArgumentParser(description="Place a limit order (USDT-M Futures).")
    parser.add_argument("symbol", type=str, help="Symbol (e.g., BTCUSDT)")
    parser.add_argument("side", choices=["BUY", "SELL"], help="BUY or SELL")
    parser.add_argument("quantity", type=float, help="Order quantity (in base asset)")
    parser.add_argument("price", type=float, help="Limit price")
    args = parser.parse_args()

    try:
        symbol = validate_symbol(args.symbol)
        client = create_binance_client()
        resp = place_order(client, symbol, args.side, "LIMIT", args.quantity, price=args.price, timeInForce="GTC")
        print("Response:", resp)
    except Exception as e:
        _log("error", "limit_order_failed", {"error": str(e)})
        raise

if __name__ == "__main__":
    main()
