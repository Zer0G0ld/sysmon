import subprocess
import json
import os
from src.utils.logger import get_logger

logger = get_logger(__name__)
CORE_BIN = os.path.expanduser("~/sysmon/bin/sysmon_core")

class CPUCollector:
    @staticmethod
    def get_usage():
        # Tenta usar o binário C primeiro
        if os.path.exists(CORE_BIN):
            try:
                output = subprocess.check_output([CORE_BIN], text=True, timeout=2)
                data = json.loads(output)
                if "cpu_pct" in data and data["cpu_pct"] != "?":
                    return {"cpu_pct": data["cpu_pct"]}
            except Exception as e:
                logger.debug(f"Falha ao usar binário C para CPU: {e}")
        
        # Fallback: tenta psutil
        try:
            import psutil
            cpu_percent = psutil.cpu_percent(interval=0.5)
            return {"cpu_pct": round(cpu_percent)}
        except ImportError:
            pass
        
        # Fallback: top
        try:
            result = subprocess.run(['top', '-bn1'], capture_output=True, text=True, timeout=2)
            for line in result.stdout.split('\n'):
                if 'CPU:' in line or 'cpu' in line.lower():
                    import re
                    match = re.search(r'(\d{1,3})%', line)
                    if match:
                        cpu_value = int(match.group(1))
                        if 0 <= cpu_value <= 100:
                            return {"cpu_pct": cpu_value}
        except Exception as e:
            logger.debug(f"Falha ao obter CPU com top: {e}")
        
        # Fallback: /proc/stat
        try:
            import time
            with open('/proc/stat', 'r') as f:
                cpu_line = f.readline().strip()
                if cpu_line.startswith('cpu '):
                    parts = cpu_line.split()
                    user = int(parts[1])
                    nice = int(parts[2])
                    system = int(parts[3])
                    idle = int(parts[4])
                    total = user + nice + system + idle
                    
                    time.sleep(0.5)
                    
                    with open('/proc/stat', 'r') as f2:
                        cpu_line2 = f2.readline().strip()
                        parts2 = cpu_line2.split()
                        user2 = int(parts2[1])
                        nice2 = int(parts2[2])
                        system2 = int(parts2[3])
                        idle2 = int(parts2[4])
                        total2 = user2 + nice2 + system2 + idle2
                        
                        if total2 > total:
                            usage = 100 * ((user2 + nice2 + system2) - (user + nice + system)) / (total2 - total)
                            return {"cpu_pct": max(0, min(100, round(usage)))}
        except Exception as e:
            logger.debug(f"Falha ao obter CPU com /proc/stat: {e}")
        
        return {"cpu_pct": "?"}
