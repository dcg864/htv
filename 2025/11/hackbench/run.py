#!/usr/bin/env python3
"""
Convenience wrapper to run HackBench from within the project directory.
Usage: python run.py [arguments]

Example: python run.py --mode reflected
"""

import sys
import os

# Add parent directory to path so imports work
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Now import and run as a module
import hackbench.cli as cli

if __name__ == '__main__':
    cli.main()
