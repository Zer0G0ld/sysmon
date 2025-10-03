import subprocess, json

def run_json(cmd):
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL)
        return json.loads(out.decode())
    except Exception:
        return {}

