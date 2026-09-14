from pathlib import Path

import pandas as pd

from src.order_class import OrderTracker


def save_active_orders(tracker: OrderTracker,output_path: str | Path) -> None:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    rows = [
        {
            "order_id": int(order.order_id),
            "price": int(order.price),
            "size": int(order.size),
            "side": getattr(order.side, "value", order.side),
            "ts_event": int(order.ts_event),
        }
        for order in tracker.orders.values()
    ]

    df = pd.DataFrame(
        rows,
        columns=["order_id", "price", "size", "side", "ts_event"]
    )

    df.to_parquet(output_path, index=False)

    print(f"Saved {len(df):,} active orders to {output_path}")