# Changelog
Todas as mudanças notáveis neste projeto serão documentadas aqui.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

---

## [Unreleased]
### Adicionado
- Planejamento para sistema de métricas históricas (SQLite/CSV).
- Planejamento para exportação de dados (JSON/CSV/API REST).
- Planejamento para monitoramento de rede (uso de dados, Wi-Fi, IP).
- Planejamento para suporte a notificações externas (Telegram, Discord, Email).
- Planejamento para interface gráfica (Tkinter, PyQt ou dashboard web).
- Planejamento para testes automatizados com `pytest`.
- Planejamento para setup automatizado (`setup.py` / `pyproject.toml`).

### Alterado
- Melhorias em andamento na coleta de CPU (percentual de uso em tempo real).
- Revisão dos módulos em `collectors` para padronização de saída JSON.
- Planejamento para otimização do log (`sysmon.log`) e rotação de arquivos.

### Corrigido
- Correção de caracteres invisíveis (NBSP) nos arquivos Python (`cpu.py` e outros).
- Padronização de indentação nos collectors para evitar SyntaxError.

---

## [0.1.0] - 2025-09-30
### Adicionado
- Estrutura inicial do projeto criada.
- Commit inicial (`first commit`) com:
  - Pasta `bin/` com launcher `sysmon`.
  - Pasta `sysmon/` com `main.py`, `notifier.py`, `config.py`, `collectors/`.
- Coleta de dados básicos:
  - CPU (`ps -A -o %cpu`)
  - Memória (`/proc/meminfo`)
  - Bateria (`termux-battery-status`)
  - Armazenamento (`df` / `termux-saf-*`)
  - Telephony (`termux-telephony-*`)
  - Location (`termux-location`)
- Sistema de notificação inicial via `sysmon-notify.sh`.
- Log centralizado em `sysmon.log`.
- Atualização do README (`Update README.md`) para documentação inicial.
- Adição de licença (`Update LICENSE`).

### Alterado
- N/A

### Corrigido
- N/A

---

