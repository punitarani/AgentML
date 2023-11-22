"""agentml package"""

from dotenv import load_dotenv

from config import PROJECT_PATH

env_loaded = load_dotenv(PROJECT_PATH.joinpath(".env"))
if not env_loaded:
    raise RuntimeError("Failed to load environment variables")
