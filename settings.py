import pathlib
import os

from dotenv import load_dotenv

load_dotenv()

TOKEN =os.getenv('DISCORD_TOKEN')
GPT_KEY = os.getenv('GPT_API_KEY')
LAVA_PASS = os.getenv('LAVA_PASS')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
GROQ_KEY = os.getenv('GROQ_KEY')
LIMEWIRE_KEY = os.getenv('LIMEWIRE_KEY')