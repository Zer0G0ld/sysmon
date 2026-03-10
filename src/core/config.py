# src/core/config.py
import json
from pathlib import Path

CONFIG_PATH = Path(__file__).parent.parent.parent / "config" / "settings.json"

def load_config():
    try:
        with open(CONFIG_PATH) as f:
            raw = json.load(f)
        config = {}
        # Mapeia a estrutura para o formato esperado pelo código
        app = raw.get("app", {})
        config["interval"] = app.get("update_interval", 10)
        config["notification_id"] = 12345   # pode ser fixo ou vir do JSON futuramente
        config["termux_activity"] = "com.termux/.app.TermuxActivity"
        # Habilita/desabilita métricas conforme config
        metrics = raw.get("metrics", {})
        config["cpu_enabled"] = metrics.get("cpu", True)
        config["memory_enabled"] = metrics.get("memory", True)
        config["battery_enabled"] = metrics.get("battery", True)
        config["storage_enabled"] = metrics.get("storage", True)
        # Temperatura é parte da bateria, então usamos o mesmo
        config["temperature_enabled"] = metrics.get("temperature", True)
        return config
    except Exception:
        # Fallback
        return {
            "interval": 10,
            "notification_id": 12345,
            "termux_activity": "com.termux/.app.TermuxActivity",
            "cpu_enabled": True,
            "memory_enabled": True,
            "battery_enabled": True,
            "storage_enabled": True,
            "temperature_enabled": True
        }

config = load_config()
