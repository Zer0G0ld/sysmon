import subprocess
import json
import os
from src.utils.logger import get_logger

logger = get_logger(__name__)
CORE_BIN = os.path.expanduser("~/sysmon/bin/sysmon_core")

class StorageCollector:
    @staticmethod
    def get_usage():
        # Tenta usar o binário C
        if os.path.exists(CORE_BIN):
            try:
                output = subprocess.check_output([CORE_BIN], text=True, timeout=2)
                data = json.loads(output)
                if "storage_total" in data and data["storage_total"] > 0:
                    total = data["storage_total"]
                    used = data["storage_used"]
                    pct = data["storage_pct"]
                    
                    # Formatação amigável
                    def human_readable(size):
                        for unit in ['B', 'KB', 'MB', 'GB']:
                            if size < 1024.0:
                                return f"{size:.1f}{unit}"
                            size /= 1024.0
                        return f"{size:.1f}TB"
                    
                    used_str = human_readable(used)
                    total_str = human_readable(total)
                    
                    return {
                        "disk": f"{used_str}/{total_str} ({pct:.1f}%)",
                        "disk_used": used_str,
                        "disk_total": total_str,
                        "disk_percent": f"{pct:.1f}%"
                    }
            except Exception as e:
                logger.debug(f"Falha ao usar binário C para armazenamento: {e}")
        
        # Fallback: comando df
        try:
            result = subprocess.run(['df', '-h', '/data'], capture_output=True, text=True, timeout=5)
            lines = result.stdout.strip().split('\n')
            if len(lines) > 1:
                parts = lines[1].split()
                if len(parts) >= 5:
                    used = parts[2]
                    total = parts[1]
                    percentage = parts[4]
                    return {
                        "disk": f"{used}/{total} ({percentage})",
                        "disk_used": used,
                        "disk_total": total,
                        "disk_percent": percentage
                    }
        except Exception as e:
            logger.debug(f"Falha ao obter storage com df: {e}")
        
        # Fallback: statvfs
        try:
            stat = os.statvfs('.')
            total = stat.f_blocks * stat.f_frsize
            free = stat.f_bfree * stat.f_frsize
            used = total - free
            percent = (used / total) * 100 if total > 0 else 0
            
            def human_readable(size):
                for unit in ['B', 'KB', 'MB', 'GB']:
                    if size < 1024.0:
                        return f"{size:.1f}{unit}"
                    size /= 1024.0
                return f"{size:.1f}TB"
            
            return {
                "disk": f"{human_readable(used)}/{human_readable(total)} ({percent:.1f}%)",
                "disk_used": human_readable(used),
                "disk_total": human_readable(total),
                "disk_percent": f"{percent:.1f}%"
            }
        except Exception as e:
            logger.error(f"Erro ao obter armazenamento: {e}")
            return {
                "disk": "?/? (?)",
                "disk_used": "?",
                "disk_total": "?",
                "disk_percent": "?"
            }
