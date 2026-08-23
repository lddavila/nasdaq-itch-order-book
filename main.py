import os
import yaml
import databento as db
from dotenv import load_dotenv
from pathlib import Path
import argparse
from datetime import datetime

def initialize_config(yaml_path="config.yaml"):
    """Loads environment variables and parses the nested configuration file."""
    # 1. Load the secret .env file if it exists locally
    load_dotenv()

    # 2. Define a custom YAML resolver tag '!env' to swap text with real system variables
    def env_var_constructor(loader, node):
        value = loader.construct_scalar(node)
        # Returns the environment variable value, or fallback empty string if missing
        return os.getenv(value, "")

    # Register the !env tag to YAML parser
    yaml.SafeLoader.add_constructor("!env", env_var_constructor)

    # 3. Read and translate the unified yaml architecture
    if not os.path.exists(yaml_path):
        raise FileNotFoundError(f"Configuration profile missing: {yaml_path}")
        
    with open(yaml_path, "r") as file:
        return yaml.safe_load(file)
def test_pipeline():
    print("--- Starting System Diagnostics ---")
    
    # 1. Test .env mapping
    load_dotenv()
    api_key = os.getenv("DATABENTO_API_KEY")
    print(f"[1/4] Checking Environment Variables... Found Key: {bool(api_key)}")
    
    # 2. Test config.yaml structural mapping
    def env_var_constructor(loader, node):
        return os.getenv(loader.construct_scalar(node), "")
    yaml.SafeLoader.add_constructor("!env", env_var_constructor)
    
    with open("config.yaml", "r") as file:
        config = yaml.safe_load(file)
    print(f"[2/4] Parsing config.yaml structure... App Name: {config['app']['name']}")

    # 3. Test Databento Connection & Package Architecture
    print("[3/4] Connecting to Databento Servers...")
    client = db.Historical(key=api_key)

    output_path = Path("/app/raw_data/AAPL_2026-07-01_mbo.dbn.zst")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 4. request some data to verify the connection
    print("[4/4] Requesting sandbox dataset...")
    data = client.timeseries.get_range(
    dataset="XNAS.ITCH",
    schema="mbo",
    symbols=["AAPL"],
    start="2026-07-01T13:30:00",
    end="2026-07-01T20:00:00")

    print(f"\nSUCCESS! Network handshake complete.")
    data.to_file(output_path)

def build_download_command_parser(sub_parsers):
    """Builds the parser for the download command."""
    download_parser = sub_parsers.add_parser(
        "download",
        help="Download market data for a specific date and symbol",
    )
    
    # Add required arguments for the download command
    download_parser.add_argument("--date", required=True, help="Date in YYYY-MM-DD format")
    download_parser.add_argument("-s", "--symbol", required=True, help="Stock symbol to download data for")
    download_parser.add_argument("-o", "--output", type=str, default=None, help="Output file path")

def build_reconstruct_command_parser(sub_parsers):
    """Builds the parser for the reconstruct command."""
    reconstruct_parser = sub_parsers.add_parser(
        "reconstruct",
        help="Reconstruct market data from downloaded files",
    )
    
    # Add required arguments for the reconstruct command
    reconstruct_parser.add_argument("--input", required=True, help="Path to the downloaded data file")
def build_parser():
    #create a parser object
    parser = argparse.ArgumentParser(description = "Download and Parse Market Data from Databento")
    #create subparsers for different commands
    sub_parsers = parser.add_subparsers(dest="command", help="Available commands", required=True)
    #create a subparser for the download command
    build_download_command_parser(sub_parsers)
    build_reconstruct_command_parser(sub_parsers)

    return parser
    
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
if __name__ == "__main__":
   parser = build_parser()
   args = parser.parse_args()

   if args.command == "download":
         if args.output is None:
            args.output = f"/app/raw_data/{args.symbol}_{args.date}_mbo.dbn.zst"
         download_stock_symbol_data(args.symbol, args.date, args.output)