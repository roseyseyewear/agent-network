#!/usr/bin/env python3
"""
Load environment variables from .env file
"""
import os
from pathlib import Path

def load_env():
    """Load environment variables from .env file"""
    env_path = Path(__file__).parent.parent / '.env'
    
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()
        print("Environment variables loaded from .env file")
    else:
        print("Warning: .env file not found")

if __name__ == "__main__":
    load_env()