import subprocess

def read():
    try:
        out = subprocess.check_output(["df","-h","/data"]).decode().splitlines()
        if len(out) >= 2:
            parts = out[1].split()
            used = parts[2]
            size = parts[1]
            perc = parts[4]
            return {"disk": f"{used}/{size} ({perc})"}
    except Exception:
        pass
    return {"disk": None}

