# SysMon Termux

Notificação persistente do sistema Android usando Termux + Termux:API.

## Funcionalidades
- Mostra uso de memória
- Status da bateria e temperatura
- Informações do SIM e operadora
- Armazenamento disponível
- CPU aproximada (via top)
- Notificação persistente com botões "Abrir Termux" e "Parar"

## Requisitos
- [Termux](https://termux.com/) (F-Droid recomendado)
- [Termux:API](https://f-droid.org/packages/com.termux.api/)
- Pacotes Termux: `termux-api`, `jq`, `coreutils`

## Como usar
```bash
chmod +x bin/sysmon-notify.sh
bin/sysmon-notify.sh
````

Para rodar em background:

```bash
nohup bin/sysmon-notify.sh > /dev/null 2>&1 &
```

Para rodar no boot:

* Instale Termux:Boot e coloque o script em `~/.termux/boot/`

## Licença 

Usando [GPL3](LICENSE)
