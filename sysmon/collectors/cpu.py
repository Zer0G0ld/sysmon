import subprocess

def read():
    """
    Lê a CPU usada via ps somando uso de todos os processos.
    Retorna: {"cpu_pct": int ou None}
    """
    try:
        result = subprocess.run(
            ["ps", "-A", "-o", "%cpu"],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            timeout=2
        )
        lines = result.stdout.splitlines()[1:]  # ignora o cabeçalho
        usage_total = sum(float(line.strip()) for line in lines if line.strip())
        usage_int = int(round(usage_total))
        return {"cpu_pct": usage_int}
    except Exception:
        return {"cpu_pct": None}

