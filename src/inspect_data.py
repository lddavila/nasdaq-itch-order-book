from collections import Counter
from itertools import islice
from pathlib import Path

import databento as db
def inspect_data(filepath, num_lines):
    """
    Inspects a market data file and prints the first few lines.

    Args:
        filepath (str): Path to the data file to inspect.
        num_lines (int): Number of lines to display from the data file.
    """
    
    print(f"Inspecting data from {filepath} and displaying the first {num_lines} lines:")
    
    store = db.DBNStore.from_file(filepath)

    print("Metadata:")
    print(store.metadata)
    print("\nFirst 10 records:")
    for record in islice(store, 10):
        print(record)

    action_counts = Counter()
    side_counts = Counter()
    record_count = 0

    for record in db.DBNStore.from_file(filepath):
        record_count += 1
        action_counts[record.action] += 1
        side_counts[record.side] += 1

    print(f"\nRecords: {record_count:,}")
    print("Actions:", action_counts)
    print("Sides:", side_counts)