import json
import os

def load_json_collection(filename: str) -> list:
    """Loads a JSON collection from the data directory."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, 'data', filename)
    
    if not os.path.exists(file_path):
        return []
        
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Only return enabled items if 'enabled' key exists
            return [item for item in data if item.get('enabled', True)]
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        return []
