import os
from dotenv import load_dotenv

load_dotenv()
APP_ID = os.getenv("APP_ID")
APP_HASH = os.getenv("APP_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
SUDO = os.getenv("SUDO")
MUST_JOIN = os.getenv("MUST_JOIN")


