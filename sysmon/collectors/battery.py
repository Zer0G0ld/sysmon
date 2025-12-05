import subprocess
import json
from sysmon.utils import run_json

def read():
    """Coleta informações da bateria via termux-api"""
    try:
        data = run_json(["termux-battery-status"])
        return {
            'battery_pct': data.get('percentage', '?'),
            'battery_status': data.get('status', '?'),
            'battery_temp': data.get('temperature', '?'),
            'battery_health': data.get('health', '?'),
            'battery_plugged': data.get('plugged', '?')
        }
    except Exception as e:
        return {
            'battery_pct': '?',
            'battery_status': 'erro',
            'battery_temp': '?',
            'battery_health': '?',
            'battery_plugged': '?'
        }