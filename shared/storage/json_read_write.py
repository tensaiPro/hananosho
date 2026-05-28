import json
import os
import logging
from datetime import datetime

def load_json(filepath, default=None):

    default = default or []

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    except FileNotFoundError:
        return default

    except json.JSONDecodeError:

        broken = (
            f"{filepath}.broken_"
            f"{datetime.now():%Y%m%d_%H%M%S}"
        )

        os.rename(filepath, broken)

        logging.exception(f"JSON破損 {filepath}")

        return default

def save_json(filepath, data):

    tmp = filepath + ".tmp"

    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

    os.replace(tmp, filepath)
