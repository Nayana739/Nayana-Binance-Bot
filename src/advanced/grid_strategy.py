import argparse
from ..utils import create_binance_client, validate_symbol, place_order, _log

def main():
    parser = argparse.ArgumentParser(description="Grid strategy (starter).")
    parser.add_argument("symbol", type=str)
    parser.add_argument("low", type=float)
    parser.add_argument("high", type=float)
    parser.add_argument("steps", type=int)
    parser.add_argument("qty", type=float)
    args = parser.parse_args()

    symbol = validate_symbol(args.symbol)
    client = create_binance_client()

    try:
        low, high = args.low, args.high
        if low >= high:
            raise ValueError("low must be less than high")

        step_size = (high - low) / args.steps
        grids = []
        for i in range(args.steps):
            buy_price = low + i * step_size
            sell_price = buy_price + step_size
            grids.append({"buy_price": round(buy_price, 2), "sell_price": round(sell_price, 2)})

        _log("info", "grid_plan", {"symbol": symbol, "grids": grids, "qty": args.qty})
        # Simulate placing the buy limits
        for g in grids:
            place_order(client, symbol, "BUY", "LIMIT", args.qty, price=g["buy_price"], timeInForce="GTC")
            # For a real grid, you'd set limit sells once buys fill or place both with logic to cancel counterpart
            _log("info", "grid_place_buy", {"grid": g})
        print({"grids": grids})
    except Exception as e:
        _log("error", "grid_failed", {"error": str(e)})
        raise

if __name__ == "__main__":
    main()
