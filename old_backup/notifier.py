import subprocess
from typing import Optional
from .config import TERMUX_ACTIVITY

class Notifier:
    def __init__(self, notif_id:int=12345):
        self.notif_id = notif_id

    def _run(self, args, input_text: Optional[str]=None):
        try:
            return subprocess.run(args, input=input_text.encode() if input_text else None,
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        except Exception as e:
            # não queremos lançar erros aqui
            return None

    def update(self, title:str, short:str, content:str):
        # usa termux-notification e passa content via stdin com --content -
        args = [
            "termux-notification",
            "--id", str(self.notif_id),
            "--title", title,
            "--content", "-",
            "--ongoing",
            "--button1", "Abrir Termux",
            "--button1-action", f"am start -n {TERMUX_ACTIVITY}",
            "--button2", "Parar",
            "--button2-action", f"termux-notification-remove {self.notif_id} && pkill -f sysmon/main.py"
        ]
        self._run(args, input_text=short + "\n\n" + content)

    def remove(self):
        self._run(["termux-notification-remove", str(self.notif_id)])

