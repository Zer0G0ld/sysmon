# SysMon v2.0

Monitoramento do sistema Android via notificação.

## 🚀 Instalação Rápida

```bash
# 1. Instale Termux e Termux:API (do F-Droid)
# 2. No Termux:
pkg update && pkg upgrade
pkg install python termux-api git
git clone [seu-repositorio]
cd sysmon
pip install psutil
python sysmon.py
```

## 📱 Como Usar

- Execute: `python sysmon.py`
- Uma notificação persistente aparecerá
- Botões na notificação:
  - Refresh: Atualiza agora
  - Stop: Para o monitor

## 🎯 Métricas Monitoradas

- Uso da CPU (%)
- Memória RAM (uso/total)
- Bateria (% e temperatura)
- Armazenamento livre

## 🔧 Executar em Background

```bash
# Iniciar em background:
nohup python sysmon.py > sysmon.log 2>&1 &

# Parar:
pkill -f sysmon.py
```

## 📝 Logs

```bash
# Ver logs:
tail -f sysmon.log
```
