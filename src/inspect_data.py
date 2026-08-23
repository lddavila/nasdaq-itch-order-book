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
    