import os
import yaml
import databento as db
from dotenv import load_dotenv
from pathlib import Path
import argparse

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
if __name__ == "__main__":
    test_pipeline()
