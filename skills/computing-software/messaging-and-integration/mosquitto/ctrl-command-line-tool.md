---
id: computing-software.messaging-and-integration.mosquitto.ctrl-command-line-tool
name: ctrl-command-line-tool
category: computing-software
field: messaging-and-integration
product: mosquitto
tags: [mosquitto-ctrl, modules, dynsec, control]
level: practitioner
status: docs-checked
description: "Run mosquitto_ctrl commands against a broker, choose a module such as dynsec and keep connection options before the module name."
sources:
  - https://mosquitto.org/man/mosquitto_ctrl-1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: configure a Mosquitto broker from the command line.

Synopsis: `mosquitto_ctrl [options | -o config-file] module-name module-command [command-options]`. Run with no module it becomes an interactive shell.

Modules:
- `dynsec`: authentication and role based access control with users and groups (Dynamic Security plugin).
- External modules: shared libraries loaded by name; module `example` loads `mosquitto_ctrl_example.so` or `mosquitto_ctrl_example.dll`, letting a plugin and module combine without recompiling Mosquitto.

Connection options mirror the other clients: `-h` (default localhost), `-p` (1883, or 8883 for TLS), `-u`, `-P`, `-i`, `-L` URL, `--unix`, `-A`, `--proxy`, `-V`, `-d`, `--quiet`, and TLS options `--cafile`, `--capath`, `--cert`, `--key`, `--ciphers`, `--insecure`, `--tls-version`, `--psk`, `--psk-identity`. A TLS connection needs `--cafile` or `--capath` for x509, or `--psk` with `--psk-identity`.

The options go before the module:

```
mosquitto_ctrl -h localhost -u admin dynsec listClients
```

An options file at `$XDG_CONFIG_HOME/mosquitto_ctrl` or `$HOME/.config/mosquitto_ctrl` (or `-o file`) holds `-option value` pairs per line. The page strongly recommends encrypted connections for all remote use.

## Checked

2026-11-03. Claims, option names, defaults and version notes were compared with the Mosquitto manual pages in `sources` (mosquitto(8), mosquitto.conf(5), mosquitto_pub, mosquitto_sub, mosquitto_rr, mosquitto_ctrl, and the Dynamic Security page where relevant). Nothing removed.

Method: documentation only; no commands were run.
