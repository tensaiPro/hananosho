from pathlib import Path
from shared.config.loader import load_yml_config

BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "configs" / "lincoln.yml"

config = load_yml_config(CONFIG_PATH)
