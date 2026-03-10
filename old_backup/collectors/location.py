import subprocess
import json
from sysmon.utils import run_json

def read():
    """Coleta informações de localização"""
    try:
        # Tenta obter localização via termux-api
        data = run_json(["termux-location", "-p", "network"])
        
        if data and 'latitude' in data and 'longitude' in data:
            lat = data.get('latitude', 0)
            lon = data.get('longitude', 0)
            accuracy = data.get('accuracy', '?')
            
            return {
                'location': f"Lat: {lat:.4f}, Lon: {lon:.4f} (±{accuracy}m)",
                'latitude': lat,
                'longitude': lon,
                'accuracy': accuracy
            }
        else:
            return {'location': 'Não disponível'}
    except Exception as e:
        return {'location': 'Erro ao obter'}