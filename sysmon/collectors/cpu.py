import subprocess
import re

def read():
    """Coleta informações da CPU"""
    try:
        # Tenta usar top para obter uso da CPU
        result = subprocess.run(['top', '-n', '1'], 
                              capture_output=True, text=True, timeout=2)
        
        # Procura por padrão de porcentagem de CPU
        lines = result.stdout.split('\n')
        for line in lines:
            # Procura por números seguidos de % (ex: "15%")
            match = re.search(r'(\d+)%', line)
            if match:
                cpu_pct = match.group(1)
                return {'cpu_pct': cpu_pct}
        
        # Fallback: lê /proc/stat
        with open('/proc/stat', 'r') as f:
            cpu_line = f.readline().strip()
            if cpu_line.startswith('cpu '):
                parts = cpu_line.split()
                # user + nice + system
                total = sum(int(p) for p in parts[1:])
                idle = int(parts[4])
                if total > 0:
                    usage = 100 * (total - idle) / total
                    return {'cpu_pct': round(usage)}
        
        return {'cpu_pct': '?'}
    except Exception as e:
        return {'cpu_pct': '?'}