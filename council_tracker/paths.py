"""Filesystem locations, resolved from this file rather than the working directory."""
from pathlib import Path

#reference locations
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
