import os

def read():
    """Coleta informações de memória"""
    try:
        with open('/proc/meminfo', 'r') as f:
            meminfo = {}
            for line in f:
                if ':' in line:
                    key, value = line.split(':', 1)
                    meminfo[key.strip()] = value.strip()
        
        mem_total = int(meminfo.get('MemTotal', '0 kB').split()[0])
        mem_available = int(meminfo.get('MemAvailable', '0 kB').split()[0])
        
        if mem_total == 0:
            mem_pct = '?'
            mem_used_mb = '?'
        else:
            mem_used = mem_total - mem_available
            mem_pct = round((mem_used / mem_total) * 100)
            mem_used_mb = round(mem_used / 1024)
        
        return {
            'mem_pct': mem_pct,
            'mem_used_mb': mem_used_mb,
            'mem_total_mb': round(mem_total / 1024),
            'mem_available_mb': round(mem_available / 1024)
        }
    except Exception as e:
        return {
            'mem_pct': '?',
            'mem_used_mb': '?',
            'mem_total_mb': '?',
            'mem_available_mb': '?'
        }