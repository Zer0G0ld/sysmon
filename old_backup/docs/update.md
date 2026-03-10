# Update Log - SysMon

Este arquivo lista melhorias pendentes, concluídas e em andamento para o projeto **SysMon**.  
Vamos marcar conforme avançarmos. ✅

---

## ✅ Concluído
- Estrutura inicial do projeto criada.
- Coleta de dados básicos (CPU, memória, bateria, armazenamento, localização e telefonia).
- Sistema de notificação simples com `sysmon-notify.sh`.
- Log centralizado em `sysmon.log`.

---

## ⏳ Em andamento
- Melhorar coleta de CPU (% de uso em tempo real).
- Revisão dos módulos `collectors` para padronização de saída JSON.
- Documentação de uso no `README.md`.

---

## 📌 Pendentes / Planejadas
- [ ] Criar **sistema de métricas históricas** (guardar dados em SQLite/CSV para análise posterior).
- [ ] Adicionar **exportação dos dados** (JSON, CSV, possivelmente API REST).
- [ ] Melhorar **notificações** (suporte a Telegram, Discord, Email além de shell script).
- [ ] Criar **interface gráfica simples** (Tkinter, PyQt ou web dashboard).
- [ ] Implementar **monitoramento de rede** (uso de dados, Wi-Fi, IP público/privado).
- [ ] Adicionar **suporte multiplataforma** (Linux, Windows, macOS).
- [ ] Otimizar `sysmon.log` (rotacionar logs, compressão, limite de tamanho).
- [ ] Criar testes automatizados (pytest).
- [ ] Automatizar build/instalação (`setup.py` ou `pyproject.toml`).

---

## 📝 Notas
- O foco inicial é melhorar a coleta e padronização de métricas.
- Quando a base estiver sólida, avançamos para exportação e interface.
- A ideia é manter tudo modular para expandir fácil.


