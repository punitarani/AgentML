"""agentml/oai.py"""

import os

from openai import OpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
assert OPENAI_API_KEY is not None, "OPENAI_API_KEY environment variable not set"

client = OpenAI(api_key=OPENAI_API_KEY)
