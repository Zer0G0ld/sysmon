import time
from src.android import battery, cpu, memory, storage, location, telephony
from src.core.notifier import Notifier
from src.core.config import config
from src.utils.logger import get_logger

logger = get_logger(__name__)

def collect_all():
    data = {}
    data.update(battery.BatteryCollector.get_status())
    data.update(cpu.CPUCollector.get_usage())
    data.update(memory.MemoryCollector.get_usage())
    data.update(storage.StorageCollector.get_usage())
    data.update(location.LocationCollector.get_location())
    data.update(telephony.TelephonyCollector.get_info())
    return data

def format_payload(data: dict):
    title = f"CPU {data.get('cpu_pct','?')} • Mem {data.get('mem_pct','?')}% • Bat {data.get('percentage','?')}%"
    short = f"CPU {data.get('cpu_pct','?')} · Mem {data.get('mem_pct','?')}% · Bat {data.get('percentage','?')}%"
    lines = []
    lines.append(f"Bateria: {data.get('percentage','?')}% ({data.get('status','?')}) Temp: {data.get('temperature','?')}°C")
    lines.append(f"Operadora: {data.get('network','?')} · SIM: {data.get('sim_state','?')}")
    lines.append(f"Memória: {data.get('mem_pct','?')}% ({data.get('mem_used_mb','?')} MB used)")
    lines.append(f"Armazenamento: {data.get('disk','?')}")
    lines.append(f"Local: {data.get('location','Não disponível')}")
    lines.append(f"Atualizado: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    content = "\n".join(lines)
    return title, short, content

def start_monitoring():
    logger.info("Iniciando monitoramento...")
    notifier = Notifier()
    interval = config.get("interval", 15)

    try:
        while True:
            try:
                data = collect_all()
                title, short, content = format_payload(data)
                logger.info(f"Atualizando notificação: {title}")
                notifier.update(title, short, content)
            except Exception as e:
                logger.error(f"Erro no ciclo principal: {e}")
                notifier.update("SysMon — erro", str(e)[:120], str(e))
            time.sleep(interval)
    except KeyboardInterrupt:
        logger.info("Monitoramento interrompido pelo usuário.")
        notifier.remove()
