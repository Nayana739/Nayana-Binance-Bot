import argparse
import time
from ..utils import create_binance_client, validate_symbol, place_order, _log

def main():
    parser = argparse.ArgumentParser(description="Simple TWAP executor.")
    parser.add_argument("symbol", type=str)
    parser.add_argument("side", choices=["BUY", "SELL"])
    parser.add_argument("total_qty", type=float)
    parser.add_argument("chunks", type=int, help="Number of time chunks")
    parser.add_argument("interval", type=int, help="Seconds between chunks")
    args = parser.parse_args()

    try:
        symbol = validate_symbol(args.symbol)
        qty_per = round(args.total_qty / args.chunks, 8)
        client = create_binance_client()
        _log("info", "twap_start", {"symbol": symbol, "side": args.side, "total_qty": args.total_qty, "chunks": args.chunks, "interval": args.interval})
        for i in range(args.chunks):
            step_info = {"step": i+1, "qty": qty_per}
            resp = place_order(client, symbol, args.side, "MARKET", qty_per)
            _log("info", "twap_step", {"step": i+1, "resp": resp})
            if i < args.chunks - 1:
                time.sleep(args.interval)
        _log("info", "twap_complete", {"symbol": symbol})
    except Exception as e:
        _log("error", "twap_failed", {"error": str(e)})
        raise

if __name__ == "__main__":
    main()
