#!/data/data/com.termux/files/usr/bin/bash
# Notificação persistente com dados do sistema (sem root)

NOTIF_ID=12345
INTERVAL=15   # segundos entre atualizações

while true; do
  # bateria
  BAT_JSON=$(termux-battery-status 2>/dev/null || echo '{}')
  BAT_PERC=$(echo "$BAT_JSON" | jq -r '.percentage // "?"')
  BAT_STATUS=$(echo "$BAT_JSON" | jq -r '.status // "unknown"')
  BAT_TEMP=$(echo "$BAT_JSON" | jq -r '.temperature // "?"')

  # telephony / sim
  TEL_JSON=$(termux-telephony-status 2>/dev/null || echo '{}')
  SIM_STATE=$(echo "$TEL_JSON" | jq -r '.simState // "?"')
  NETWORK=$(echo "$TEL_JSON" | jq -r '.networkOperatorName // "?"')

  # memória
  MEM_TOTAL_kb=$(awk '/MemTotal/{print $2}' /proc/meminfo 2>/dev/null || echo 0)
  MEM_FREE_kb=$(awk '/MemAvailable/{print $2}' /proc/meminfo 2>/dev/null || echo 0)
  if [ "$MEM_TOTAL_kb" -eq 0 ]; then
    MEM_PERC="?"
  else
    used_kb=$((MEM_TOTAL_kb - MEM_FREE_kb))
    MEM_PERC=$(( used_kb * 100 / MEM_TOTAL_kb ))
  fi

  # armazenamento
  DISK_USED=$(df -h /data | awk 'NR==2{print $3 "/" $2 " (" $5 ")"}' 2>/dev/null)

  # CPU aproximada (top 1 linha)
  CPU_LINE=$(top -n 1 | head -n 1)
  CPU_PERC=$(echo "$CPU_LINE" | grep -o '[0-9]\+%' | head -n1)

  # montar título e conteúdo
  TITLE="Sistema — CPU ${CPU_PERC:-?} • Mem ${MEM_PERC}% • Bat ${BAT_PERC}%"
  SHORT="CPU ${CPU_PERC:-?} · Mem ${MEM_PERC}% · Bat ${BAT_PERC}% · SIM ${SIM_STATE}"

  BIG="Bateria: ${BAT_PERC}% (${BAT_STATUS}), Temp: ${BAT_TEMP}°C\n"
  BIG+="Rede: ${NETWORK}\nSIM: ${SIM_STATE}\n"
  BIG+="Memória: ${MEM_PERC}% (${used_kb:-?} KB used)\n"
  BIG+="Armazenamento: ${DISK_USED}\n"
  BIG+="Atualizado: $(date '+%Y-%m-%d %H:%M:%S')\n"
  BIG+="(Toque para abrir Termux. Botões: registrar / parar)\n"

  # atualizar notificação
  printf "%s\n\n%s" "$SHORT" "$BIG" | termux-notification \
    --id $NOTIF_ID \
    --title "$TITLE" \
    --content - \
    --ongoing \
    --button1 "Abrir Termux" \
    --button1-action "am start -n com.termux/com.termux.app.TermuxActivity" \
    --button2 "Parar" \
    --button2-action "termux-notification-remove $NOTIF_ID && pkill -f sysmon-notify.sh" \
    2>/dev/null

  sleep $INTERVAL
done
