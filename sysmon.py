#!/data/data/com.termux/files/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.core.monitor import start_monitoring

if __name__ == "__main__":
    start_monitoring()
