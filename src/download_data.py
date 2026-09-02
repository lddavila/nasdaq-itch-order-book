
from dotenv import load_dotenv
import os
from pathlib import Path
import databento as db
from datetime import date, timedelta
def download_stock_symbol_data(symbol,date_string,output,start_time,end_time):
    
    """Downloads market data for a specific stock symbol and date."""
    # Load environment variables
    load_dotenv()

    
    api_key = os.getenv("DATABENTO_API_KEY")
    
    # Initialize Databento client
    client = db.Historical(key=api_key)
    
    # Define the output path
    if os.path.exists(output):
        print(f"Warning: The output file {output} already exists and the download will be skipped. Please specify a different output path if you wish to redownload the data.")
        return

    trading_day = date.fromisoformat(date_string)
    following_day = trading_day + timedelta(days=1)

    start = f"{trading_day.isoformat()}T00:00:00Z"
    end = f"{following_day.isoformat()}T00:00:00Z"

    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    # Request data from Databento
    try:
        data = client.timeseries.get_range(
            dataset="XNAS.ITCH",
            schema="mbo",
            symbols=[symbol],
            start=start,
            end=end
        )
    except Exception as e:
        print(f"Error downloading data for {symbol} on {date_string}: {e}")
        return
    print(f"successfully downloaded data to destination {output_path}.")

    # Save the data to the specified output file
    data.to_file(output_path)
    print(f"Data for {symbol} on {date} has been downloaded to {output_path}")