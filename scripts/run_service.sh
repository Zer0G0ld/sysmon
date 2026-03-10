#!/data/data/com.termux/files/usr/bin/bash
cd "$(dirname "$0")/.."
nohup python sysmon.py > sysmon.log 2>&1 &
echo $! > .sysmon.pid
echo "SysMon rodando em background. PID: $(cat .sysmon.pid)"
echo "Ver logs: tail -f sysmon.log"
