import subprocess
import json
from sysmon.utils import run_json

def read():
    """Coleta informações de telefonia/SIM"""
    try:
        data = run_json(["termux-telephony-status"])
        return {
            'sim_state': data.get('simState', '?'),
            'network': data.get('networkOperatorName', '?'),
            'phone_number': data.get('phoneNumber', '?'),
            'device_id': data.get('deviceId', '?'),
            'network_type': data.get('networkType', '?')
        }
    except Exception as e:
        return {
            'sim_state': '?',
            'network': '?',
            'phone_number': '?',
            'device_id': '?',
            'network_type': '?'
        }