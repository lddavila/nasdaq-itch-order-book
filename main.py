import os
import yaml
import databento as db
from dotenv import load_dotenv

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

if __name__ == "__main__":
    # Bootstrapping the configuration mapping
    config = initialize_config()

    # Accessing config data directly
    app_name = config["app"]["name"]
    api_key = config["services"]["weather_api"]["api_key"]
    db_pass = config["database"]["password"]

    print(f"--- Launching {app_name} ---")
    print(f"API Key successfully retrieved: {bool(api_key)} (Length: {len(api_key)})")
    print(f"Database password loaded into RAM: {bool(db_pass)}")