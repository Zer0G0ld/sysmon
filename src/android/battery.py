import subprocess
import json
from src.utils.logger import get_logger

logger = get_logger(__name__)

class BatteryCollector:
    @staticmethod
    def get_status():
        try:
            output = subprocess.check_output(["termux-battery-status"], text=True, timeout=5)
            data = json.loads(output)
            return {
                "percentage": data.get("percentage", "?"),
                "status": data.get("status", "?"),
                "temperature": data.get("temperature", "?"),
                "health": data.get("health", "?"),
                "plugged": data.get("plugged", "?")
            }
        except subprocess.TimeoutExpired:
            logger.error("Timeout ao obter status da bateria")
        except Exception as e:
            logger.error(f"Erro ao obter status da bateria: {e}")
        return {
            "percentage": "?",
            "status": "erro",
            "temperature": "?",
            "health": "?",
            "plugged": "?"
        }
