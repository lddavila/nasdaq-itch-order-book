from collections import Counter
from copy import error
from pathlib import Path
import databento as db
from src.order_book import OrderBook
from src.store_unpacked_data import save_active_orders

def reconstruct_data(file_path: str | Path, output_path: str | Path) -> OrderBook:
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    book = OrderBook()
    action_counts = Counter()
    record_count = 0

    store = db.DBNStore.from_file(file_path)
    print(store)
    for record_count, message in enumerate(store,start=1):
        
        action_counts[message.action] += 1
        
        try:
           book.apply(message)
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
        print(f"Active orders: {len(book.tracker.orders):,}")
        print(f"Actions: {dict(action_counts)}")

        if record_count % 100_000 == 0:
            book.validate()
            

        # Save the reconstructed data to the output path
    save_active_orders(book.tracker, output_path)
    print(f"Processed records: {record_count:,}")
    print(f"Active orders: {len(book.tracker):,}")
    print(f"Bid levels: {len(book.bids):,}")
    print(f"Ask levels: {len(book.asks):,}")
    print(f"Action counts: {dict(action_counts)}")

    return book.tracker