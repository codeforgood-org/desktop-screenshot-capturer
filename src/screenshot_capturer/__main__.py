"""
Entry point for running the package as a module.

Allows running with: python -m screenshot_capturer
"""

import sys
from .cli import main

if __name__ == "__main__":
    sys.exit(main())
