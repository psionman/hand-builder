# constants.py

"""Constants for Hand builder."""

from pathlib import Path

from appdirs import user_config_dir, user_data_dir
from psiutils.known_paths import resolve_path

from hand_builder import __app_name__, __author__

# General
HTML_DIR = resolve_path("html", __file__)
HELP_URI = ""

# Paths
CONFIG_PATH = Path(user_config_dir(__app_name__, __author__), "config.toml")
USER_DATA_DIR = Path(user_data_dir(__app_name__, __author__))
USER_DATA_DIR.mkdir(exist_ok=True)

USER_DATA_FILE = Path(USER_DATA_DIR, "data.json")

# GUI
APP_TITLE = "Hand builder"
ICON_FILE = Path(Path(__file__).parent, "images", "icon.png")
DEFAULT_GEOMETRY = "300x250"
