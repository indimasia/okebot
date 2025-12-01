import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot configuration
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
if not DISCORD_TOKEN:
    raise ValueError("DISCORD_TOKEN not found in environment variables")

# Bot settings
BOT_PREFIX = os.getenv('BOT_PREFIX', '!oke ')  # Default: "!oke " (with space)
BOT_NAME = os.getenv('BOT_NAME', 'OKEbot')
BOT_VERSION = os.getenv('BOT_VERSION', '1.0.0')

# Supabase configuration
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Supabase configuration not found in environment variables")