import subprocess
import json
from src.utils.logger import get_logger

logger = get_logger(__name__)

class TelephonyCollector:
    @staticmethod
    def get_info():
        try:
            output = subprocess.check_output(["termux-telephony-status"], text=True, timeout=5)
            data = json.loads(output)
            return {
                "sim_state": data.get('simState', '?'),
                "network": data.get('networkOperatorName', '?'),
                "phone_number": data.get('phoneNumber', '?'),
                "device_id": data.get('deviceId', '?'),
                "network_type": data.get('networkType', '?')
            }
        except Exception as e:
            logger.error(f"Erro ao obter informações de telefonia: {e}")
            return {
                "sim_state": '?',
                "network": '?',
                "phone_number": '?',
                "device_id": '?',
                "network_type": '?'
            }
