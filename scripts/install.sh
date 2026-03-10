#!/data/data/com.termux/files/usr/bin/bash
echo "📦 Instalando SysMon..."
#pkg update && pkg upgrade -y
#pkg install python termux-api clang -y
#pip install psutil

# Criar diretório bin
mkdir -p ~/sysmon/bin

# Compilar o módulo C
echo "🔧 Compilando módulo C..."
cd ~/sysmon/src/c
clang -O2 -o ~/sysmon/bin/sysmon_core sysmon_core.c

# Dar permissões
chmod +x ~/sysmon/bin/sysmon_core
chmod +x ~/sysmon/sysmon.py
chmod +x ~/sysmon/scripts/*.sh

echo ""
echo "✅ Instalação completa!"
echo ""
echo "📱 Para executar:"
echo "   python ~/sysmon/sysmon.py"
echo ""
echo "🔄 Para rodar em background:"
echo "   ~/sysmon/scripts/run_service.sh"
echo ""
echo "📊 Para ver logs:"
echo "   tail -f ~/sysmon/sysmon.log"
