import argparse
from datetime import datetime

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