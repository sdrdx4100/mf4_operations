"""
Main entry point for MF4 Operations application
"""

import sys
import logging
from .gui import run_gui


def main():
    """Main entry point"""
    try:
        run_gui()
    except KeyboardInterrupt:
        print("\nApplication closed by user")
        sys.exit(0)
    except Exception as e:
        logging.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
