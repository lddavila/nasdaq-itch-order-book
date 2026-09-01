from collections import Counter
from copy import error
from pathlib import Path
import databento as db
from src.order_class import OrderTracker

def reconstruct_data(file_path: str | Path, output_path: str | Path) -> OrderTracker:
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    tracker = OrderTracker()
    action_counts = Counter()
    record_count = 0

    store = db.DBNStore.from_file(file_path)
    for record_count, message in enumerate(store,start=1):
        
        action_counts[message.action] += 1
        try:
            tracker.apply(message)
        except (KeyError, ValueError) as e:
            raise RuntimeError("Order reconstruction failed:\n"
                               f" record: {record_count:,}\n"
                               f" action: {message.action}\n"
                               f" order_id: {message.order_id}\n"
                               f" size: {message.size}\n"
                               f" price: {message.price}\n"
                               f" ts_event: {message.ts_event}\n"
                               f" sequence: {message.sequence}"
            ) from error
        print(f"Processed records: {record_count:,}")
        print(f"Active orders: {len(tracker.orders):,}")
        print(f"Actions: {dict(action_counts)}")

        # Save the reconstructed data to the output path
        tracker.save(output_path)
        return tracker