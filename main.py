import argparse
from datetime import datetime   
from src.download_data import download_stock_symbol_data
from src.parser_logic import build_parser    
from src.reconstruct_data import reconstruct_data
from src.inspect_data import inspect_data

if __name__ == "__main__":
   parser = build_parser()
   args = parser.parse_args()

   if args.command == "download":
         if args.output is None:
            args.output = f"/app/raw_data/{args.symbol}_{args.date}_mbo.dbn.zst"
         if args.start_time is None:
            args.start_time = "T13:30:00"
         if args.end_time is None:
            args.end_time = "T20:00:00"
         download_stock_symbol_data(args.symbol, args.date, args.output, args.start_time, args.end_time)
   if args.command == "inspect":
        inspect_data(args.filepath, args.num_lines)
   if args.command == "reconstruct":
        reconstruct_data(args.filepath, args.output)