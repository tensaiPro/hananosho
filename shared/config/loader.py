from pathlib import Path
import yaml
import logging


def load_yml_config(config_path: Path) -> dict:
    """
    YAML設定ファイル読込
    """

    try:

        with open(config_path, encoding="utf-8" ) as yml:
            return yaml.safe_load(yml)

    except FileNotFoundError:
        logging.exception(f"設定ファイルなし: {config_path}")
        raise

    except yaml.YAMLError:
        logging.exception(f"yaml読込失敗: {config_path}")
        raise
