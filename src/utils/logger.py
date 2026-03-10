# src/utils/logger.py
import logging
import sys
from pathlib import Path

LOG_FILE = Path(__file__).parent.parent.parent / "sysmon.log"

def setup_logger(name=__name__):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Handler para arquivo
    fh = logging.FileHandler(LOG_FILE)
    fh.setLevel(logging.INFO)

    # Handler para console
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger

def get_logger(name=__name__):
    return logging.getLogger(name)

# Inicializa o logger uma vez (opcional, mas pode chamar explicitamente no monitor)
# setup_logger()
