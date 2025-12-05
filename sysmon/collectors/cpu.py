import subprocess
import re

def read():
    """Coleta informações da CPU"""
    try:
        # Método mais confiável: usa psutil se disponível
        try:
            import psutil
            cpu_percent = psutil.cpu_percent(interval=0.5)
            return {'cpu_pct': round(cpu_percent)}
        except ImportError:
            pass
        
        # Fallback: método simplificado
        result = subprocess.run(['top', '-bn1'], 
                              capture_output=True, text=True, timeout=2)
        
        # Procura linha de CPU
        for line in result.stdout.split('\n'):
            if 'CPU:' in line or 'cpu' in line.lower():
                # Procura padrões como: "CPU: 15%"
                match = re.search(r'(\d{1,3})%', line)
                if match:
                    cpu_value = int(match.group(1))
                    if 0 <= cpu_value <= 100:  # Validação
                        return {'cpu_pct': cpu_value}
        
        # Último fallback: /proc/stat
        with open('/proc/stat', 'r') as f:
            cpu_line = f.readline().strip()
            if cpu_line.startswith('cpu '):
                parts = cpu_line.split()
                user = int(parts[1])
                nice = int(parts[2])
                system = int(parts[3])
                idle = int(parts[4])
                total = user + nice + system + idle
                
                # Lê novamente após 0.5s para cálculo
                import time
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
                        return {'cpu_pct': max(0, min(100, round(usage)))}
        
        return {'cpu_pct': '?'}
    except Exception as e:
        return {'cpu_pct': '?'}