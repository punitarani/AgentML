"""agentml package"""

import os

from dotenv import load_dotenv

from config import PROJECT_PATH

from .manager import Manager

__all__ = ["Manager"]

env_loaded = load_dotenv(PROJECT_PATH.joinpath(".env"))
if not env_loaded:
    raise RuntimeError("Failed to load environment variables")

if not os.getenv("PYTHON_EXE"):
    raise RuntimeError("PYTHON_EXE environment variable not set")
