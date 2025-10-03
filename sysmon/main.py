#!/data/data/com.termux/files/usr/bin/env python3
"""
Entry point for SysMon Termux (no root required).
"""

import time
import sys
from sysmon.config import INTERVAL, NOTIF_ID
from sysmon.collectors import battery, telephony, memory, storage, cpu, location
from sysmon.notifier import Notifier

def log(msg):
    print(f"[sysmon] {msg}", file=sys.stderr, flush=True)

def gather():
    data = {}
    data.update(battery.read())
    data.update(telephony.read())
    data.update(memory.read())
    data.update(storage.read())
    data.update(cpu.read())   # cpu may be approximate
    data.uodate(location())
    return data

def format_payload(d: dict):
    title = f"CPU {d.get('cpu_pct','?')} • Mem {d.get('mem_pct','?')}% • Bat {d.get('battery_pct','?')}%"
    short = f"CPU {d.get('cpu_pct','?')} · Mem {d.get('mem_pct','?')}% · Bat {d.get('battery_pct','?')}%"
    big = []
    big.append(f"Bateria: {d.get('battery_pct','?')}% ({d.get('battery_status','?')}) Temp: {d.get('battery_temp','?')}°C")
    big.append(f"Operadora: {d.get('network','?')} · SIM: {d.get('sim_state','?')}")
    big.append(f"Memória: {d.get('mem_pct','?')}% ({d.get('mem_used_kb','?')} KB used)")
    big.append(f"Armazenamento: {d.get('disk','?')}")
    big.append(f"Atualizado: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    content = "\n".join(big)
    return title, short, content

def main():
    log("Main loop iniciado")
    notifier = Notifier(notif_id=NOTIF_ID)
    while True:
        try:
            data = gather()
            title, short, big = format_payload(data)
            log(f"Payload: {title}")
            notifier.update(title=title, short=short, content=big)
        except Exception as e:
            # não quebrar o loop; reporta em notificação curta
            notifier.update(title="SysMon — erro", short=str(e)[:120], content=str(e))
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()

