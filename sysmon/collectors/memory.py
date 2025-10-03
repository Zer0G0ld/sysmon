def read():
    try:
        with open("/proc/meminfo","r") as f:
            data = f.read().splitlines()
        mem = {}
        for line in data:
            if line.startswith("MemTotal:"):
                mem["total_kb"] = int(line.split()[1])
            if line.startswith("MemAvailable:"):
                mem["avail_kb"] = int(line.split()[1])
        total = mem.get("total_kb",0)
        avail = mem.get("avail_kb",0)
        used = total - avail if total else 0
        pct = int(used * 100 / total) if total else None
        return {
            "mem_total_kb": total,
            "mem_used_kb": used,
            "mem_pct": pct
        }
    except Exception:
        return {"mem_pct": None}

