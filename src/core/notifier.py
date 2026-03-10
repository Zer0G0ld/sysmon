import subprocess
from typing import Optional
from src.core.config import config
from src.utils.logger import get_logger

logger = get_logger(__name__)

class Notifier:
    def __init__(self, notif_id: int = None):
        self.notif_id = notif_id or config.get("notification_id", 12345)
        self.termux_activity = config.get("termux_activity", "com.termux/.app.TermuxActivity")

    def _run(self, args, input_text: Optional[str] = None):
        try:
            return subprocess.run(args, input=input_text.encode() if input_text else None,
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False, timeout=5)
        except Exception as e:
            logger.error(f"Erro ao executar comando: {e}")
            return None

    def update(self, title: str, short: str, content: str):
        args = [
            "termux-notification",
            "--id", str(self.notif_id),
            "--title", title,
            "--content", "-",
            "--ongoing",
            "--button1", "Abrir Termux",
            "--button1-action", f"am start -n {self.termux_activity}",
            "--button2", "Parar",
            "--button2-action", f"termux-notification-remove {self.notif_id} && pkill -f sysmon.py"
        ]
        self._run(args, input_text=short + "\n\n" + content)

    def remove(self):
        self._run(["termux-notification-remove", str(self.notif_id)])
