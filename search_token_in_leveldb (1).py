import os
import re
import sys
import logging
from pathlib import Path

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Regular expression pattern to match token format
pattern = re.compile(rb"OTc0ODkzMzczMjA5MDU1MzA0\.GAeG2Q\.[A-Za-z0-9\-]+")  # Adjust pattern as needed

def search_in_leveldb(directory_path):
    """Search for tokens in LevelDB files."""
    found_tokens = []
    
    # Iterate through all .ldb and .log files in the specified directory
    for file_name in os.listdir(directory_path):
        if file_name.endswith(('.ldb', '.log')):
            file_path = Path(directory_path) / file_name
            try:
                with open(file_path, 'rb') as file:  # Open in binary mode
                    content = file.read()
                    matches = pattern.findall(content)
                    if matches:
                        decoded_tokens = [token.decode('utf-8', errors='ignore') for token in matches]
                        found_tokens.extend(decoded_tokens)
                        logging.info(f"Tokens found in {file_name}: {', '.join(decoded_tokens)}")
            except (OSError, IOError) as e:
                logging.error(f"Error reading {file_path}: {e}")
    
    return found_tokens

def get_leveldb_path():
    """Get the path to the LevelDB folder."""
    base_path = Path.home() / "AppData" / "Local" / "Google" / "Chrome" / "User Data" / "Default" / "Local Storage" / "leveldb"
    if base_path.exists():
        return base_path
    else:
        logging.error(f"LevelDB folder not found at {base_path}. Please check your Chrome installation.")
        sys.exit(1)

def main():
    """Main function to execute the script."""
    directory_path = get_leveldb_path()
    found_tokens = search_in_leveldb(directory_path)

    if not found_tokens:
        logging.info("No tokens found in any files.")
    else:
        logging.info(f"\nTotal tokens found: {len(found_tokens)}")
        logging.info(f"Tokens: {found_tokens}")

    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
