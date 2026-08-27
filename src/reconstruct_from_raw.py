from collections import Counter
from itertools import islice
from pathlib import Path

import databento as db

def reconstruct_data(filepath, output):
    """
    Reconstruct market data from a raw data file.

    Args:
        filepath (str): Path to the raw data file to reconstruct.
        output (str): Path to save the reconstructed data.
    """
    
    print(f"Reconstructing data from {filepath} and saving to {output}")

    #read the raw data file using DBNStore
    store = db.DBNStore.from_file(filepath)
    