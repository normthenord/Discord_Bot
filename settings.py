import pathlib
import os

from dotenv import load_dotenv

load_dotenv()

TOKEN =os.getenv('DISCORD_TOKEN')
GPT_KEY = os.getenv('GPT_API_KEY')
LAVA_PASS = os.getenv('LAVA_PASS')