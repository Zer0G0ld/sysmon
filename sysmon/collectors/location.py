import subprocess, json

def read():
    try:
        result = subprocess.run(
            ["termux-location"],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            timeout=3
        )
        data = json.loads(result.stdout)
        return {
            "lat": data.get("latitude"),
            "lon": data.get("longitude"),
            "alt": data.get("altitude"),
            "acc": data.get("accuracy")
        }
    except Exception:
        return {}

