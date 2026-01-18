#!/usr/bin/env python3
"""
Robot Framework MCP Server - Entry Point
This file provides backward compatibility with the original entry point.
The main implementation is now in src/server.py
"""

import sys
import os

# Add src directory to path
src_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
if src_dir not in sys.path:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import and run from new location
from src.server import main

if __name__ == "__main__":
    main()
