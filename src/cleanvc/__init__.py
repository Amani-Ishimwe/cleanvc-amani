"""cleanvc - Effortless CSV cleanup utility."""

__version__ = "0.1.0"

from .cleaner import CSVCleaner, slugify_header
from .cli import main

__all__ = ["CSVCleaner", "slugify_header", "main", "__version__"]
