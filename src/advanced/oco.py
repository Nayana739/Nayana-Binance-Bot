import argparse
from ..utils import create_binance_client, validate_symbol, place_order, _log

def main():
    parser = argparse.ArgumentParser(description="Simulated OCO (take-profit + stop-loss).")
    parser.add_argument("symbol", type=str)
    parser.add_argument("side", choices=["BUY", "SELL"])
    parser.add_argument("quantity", type=float)
    parser.add_argument("take_profit", type=float)
    parser.add_argument("stop_loss", type=float)
    args = parser.parse_args()

    symbol = validate_symbol(args.symbol)
    client = create_binance_client()

    try:
        # Place a market entry (simulated in dry-run)
        entry_resp = place_order(client, symbol, args.side, "MARKET", args.quantity)
        _log("info", "oco_entry", {"entry_resp": entry_resp})

        # Place TP: use TAKE_PROFIT_MARK or LIMIT in simulation/live depending on API support
        tp_side = "SELL" if args.side == "BUY" else "BUY"
        sl_side = tp_side

        # take profit order (LIMIT)
        tp_resp = place_order(client, symbol, tp_side, "LIMIT", args.quantity, price=args.take_profit, timeInForce="GTC", reduceOnly=True)
        _log("info", "oco_take_profit", {"tp_resp": tp_resp})

        # stop loss order (STOP_MARKET)
        sl_resp = place_order(client, symbol, sl_side, "STOP_MARKET", args.quantity, stop_price=args.stop_loss, reduceOnly=True)
        _log("info", "oco_stop_loss", {"sl_resp": sl_resp})

        print({"entry": entry_resp, "tp": tp_resp, "sl": sl_resp})

    except Exception as e:
        _log("error", "oco_failed", {"error": str(e)})
        raise

if __name__ == "__main__":
    main()
