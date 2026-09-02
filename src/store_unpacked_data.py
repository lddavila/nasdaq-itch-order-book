from dataclasses import asdict
from pathlib import Path

import pandas as pd

from src.order_class import OrderTracker

def save_active_orders(tracker:OrderTracker, output_path: str | Path) -> None:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True,exist_ok=True)
    rows = [asdict(order) for order in tracker.orders.values()]
    dataframe = pd.DataFrame(rows,columns=["order_id","price","size","side","ts_event"])
    dataframe.to_csv(output_path, index=False)

    dataframe.to_parquet(output_path,index=False)
    print(f"Saved {len(dataframe):,} active orders "
          f"to {output_path} in CSV and Parquet formats.")