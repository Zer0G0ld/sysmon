from ..utils import run_json

def read():
    j = run_json(["termux-battery-status"])
    return {
        "battery_pct": j.get("percentage"),
        "battery_status": j.get("status"),
        "battery_temp": j.get("temperature")
    }

