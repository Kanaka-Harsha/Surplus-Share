import os
from dotenv import load_dotenv
load_dotenv(override=True)
class Settings():
    DATABASE_URL=os.getenv("DATABASE_URL")
settings=Settings()