"""config.py"""

from pathlib import Path

PROJECT_PATH = Path(__file__).parent

DATA_DIR = PROJECT_PATH.joinpath("data")
LOGS_DIR = PROJECT_PATH.joinpath("logs")
if not LOGS_DIR.exists():
    LOGS_DIR.mkdir()

SANDBOX_DIR = PROJECT_PATH.joinpath(".sandbox")
if not SANDBOX_DIR.exists():
    SANDBOX_DIR.mkdir()
