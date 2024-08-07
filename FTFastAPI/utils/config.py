import os
from dotenv import load_dotenv

class Config:
    """Config class to handle loading environment variables."""

    def __init__(self):
        load_dotenv()
        self.DATABASE_URL = os.getenv("DATABASE_URL")

        if not self.DATABASE_URL:
            raise ValueError("DATABASE_URL environment variable is not set")

config = Config()
