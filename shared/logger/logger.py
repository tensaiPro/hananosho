import os
import logging
from datetime import datetime

def setup_logging(log_dir: Path):
    """
    ロギング設定
    """

    log_dir.mkdir(exist_ok=True)

    log_filename = datetime.now().strftime("%Y-%m-%d") + ".log"
    log_path = log_dir / log_filename

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        encoding="utf-8",
        handlers=[
            logging.FileHandler(log_path, encoding="utf-8"),
            logging.StreamHandler()
        ]
    )
