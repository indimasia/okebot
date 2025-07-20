import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot configuration
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
if not DISCORD_TOKEN:
    raise ValueError("DISCORD_TOKEN not found in environment variables")

# Bot settings
BOT_PREFIX = os.getenv('BOT_PREFIX')
BOT_NAME = os.getenv('BOT_NAME')
BOT_VERSION = os.getenv('BOT_VERSION')