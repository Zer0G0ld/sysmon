import subprocess
import json
from src.utils.logger import get_logger

logger = get_logger(__name__)

class LocationCollector:
    @staticmethod
    def get_location():
        try:
            output = subprocess.check_output(["termux-location", "-p", "network"], text=True, timeout=10)
            data = json.loads(output)
            if data and 'latitude' in data and 'longitude' in data:
                lat = data.get('latitude', 0)
                lon = data.get('longitude', 0)
                accuracy = data.get('accuracy', '?')
                return {
                    "location": f"Lat: {lat:.4f}, Lon: {lon:.4f} (±{accuracy}m)",
                    "latitude": lat,
                    "longitude": lon,
                    "accuracy": accuracy
                }
            else:
                return {"location": "Não disponível"}
        except subprocess.TimeoutExpired:
            logger.error("Timeout ao obter localização")
        except Exception as e:
            logger.error(f"Erro ao obter localização: {e}")
        return {"location": "Erro ao obter"}
