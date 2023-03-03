from dotenv import load_dotenv
import os
import dacite
import yaml
from src.base import Config

load_dotenv()

# load config.yaml
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
CONFIG: Config = dacite.from_dict(
    Config, yaml.safe_load(
        open(os.path.join(SCRIPT_DIR, "./../config", os.environ["CONFIG_FILE"]), "r"))
)

BOT_INSTRUCTIONS = CONFIG.instructions
EXAMPLE_CONVOS = CONFIG.example_conversations
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
MAX_TOKEN = int(os.environ["MAX_TOKEN"])
