"""Compatibility config matching the requested project structure.

The Pytest fixtures import settings from config.py because this filename is
not a normal Python module name.
"""

from config import BASE_URL, BROWSER, DEFAULT_TIMEOUT, HEADLESS, SLOW_MO, VIEWPORT
