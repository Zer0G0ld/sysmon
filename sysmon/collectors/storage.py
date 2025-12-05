import subprocess
import os

def read():
    """Coleta informações de armazenamento"""
    try:
        # Usa df para obter informações do armazenamento
        result = subprocess.run(['df', '-h', '/data'], 
                              capture_output=True, text=True)
        lines = result.stdout.strip().split('\n')
        if len(lines) > 1:
            parts = lines[1].split()
            if len(parts) >= 5:
                used = parts[2]
                total = parts[1]
                percentage = parts[4]
                return {
                    'disk': f"{used}/{total} ({percentage})",
                    'disk_used': used,
                    'disk_total': total,
                    'disk_percent': percentage
                }
        
        # Fallback: verifica espaço livre no diretório atual
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
            'disk': f"{human_readable(used)}/{human_readable(total)} ({percent:.1f}%)",
            'disk_used': human_readable(used),
            'disk_total': human_readable(total),
            'disk_percent': f"{percent:.1f}%"
        }
    except Exception as e:
        return {
            'disk': '?/? (?)',
            'disk_used': '?',
            'disk_total': '?',
            'disk_percent': '?'
        }