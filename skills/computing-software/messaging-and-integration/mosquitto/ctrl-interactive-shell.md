---
id: computing-software.messaging-and-integration.mosquitto.ctrl-interactive-shell
name: ctrl-interactive-shell
category: computing-software
field: messaging-and-integration
product: mosquitto
tags: [mosquitto-ctrl-shell, interactive, dynsec-mode, broker-mode, shell]
level: practitioner
status: docs-checked
description: "Use the mosquitto_ctrl interactive shell: auth, connect, dynsec and broker modes, tab completion and help."
sources:
  - https://mosquitto.org/man/mosquitto_ctrl_shell-1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: drive broker configuration interactively.

Start the shell by running `mosquitto_ctrl` with no module or command. Example workflow:

```
$ mosquitto_ctrl
> auth
username: admin
password:
> connect mqtt://localhost
mqtt://localhost:1883> dynsec
mqtt://localhost:1883|dynsec> createGroup newgroup
OK
```

Modes:
- Pre-connection: set authentication, connect, read help and exit.
- Post-connection: switch between modules, view help or exit.
- `dynsec`: create, delete and modify users, groups, roles and ACLs. Works only if the broker has the Dynamic Security plugin loaded and you have permission.
- `broker`: only works if `enable_control_api` is true; it has `listListeners` and `listPlugins`.
- Leave a mode with `return`; leave the shell with `exit`.

Authentication: `-u`/`-P` on the command line, or `auth` (prompts for both) or `auth username` (prompts for the password in the shell). x509 client certificates are also supported.

Connecting: `connect` (localhost:1883), `connect mqtt://host`, `connect mqtt://host:1884`, `connect mqtts://host` for TLS, `ws://` and `wss://` for WebSockets. Using `-h` on the command line connects immediately.

Tab twice lists commands or arguments; usernames, groups and roles autocomplete. `help createGroup` shows help. History uses the arrow keys and is not saved to disk.

## Checked

2026-11-08. Confirmed against the mosquitto_ctrl_shell man page: shell start, example workflow, the four modes, broker mode needing enable_control_api, auth and connect forms, tab completion, help and unsaved history. Claims unchanged.

Method: documentation only; no commands were run.
