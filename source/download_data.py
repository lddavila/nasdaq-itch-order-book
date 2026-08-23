
from dotenv import load_dotenv
import os
from pathlib import Path
import databento as db
import yaml
def download_stock_symbol_data(symbol,date,output):
    
    """Downloads market data for a specific stock symbol and date."""
    # Load environment variables
    load_dotenv()

    
    api_key = os.getenv("DATABENTO_API_KEY")
    
    # Initialize Databento client
    client = db.Historical(key=api_key)
    
    # Define the output path
    if os.path.exists(output):
        print(f"Warning: The output file {output} already exists and the download will be skipped. Please specify a different output path if you wish to redownload the data.")
    else:
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        # Request data from Databento
        try:
            data = client.timeseries.get_range(
                dataset="XNAS.ITCH",
                schema="mbo",
                symbols=[symbol],
                start=f"{date}T13:30:00",
                end=f"{date}T20:00:00"
            )
        except Exception as e:
            print(f"Error downloading data for {symbol} on {date}: {e}")
            return
        print(f"successfully downloaded data to destination {output_path}.")
    
        # Save the data to the specified output file
        data.to_file(output_path)
        print(f"Data for {symbol} on {date} has been downloaded to {output_path}")