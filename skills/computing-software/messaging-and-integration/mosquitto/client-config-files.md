---
id: computing-software.messaging-and-integration.mosquitto.client-config-files
name: client-config-files
category: computing-software
field: messaging-and-integration
product: mosquitto
tags: [client-config, xdg-config-home, option-files]
level: practitioner
status: docs-checked
description: "Keep mosquitto_pub, sub and ctrl options in a per-tool config file and override them from the command line."
sources:
  - https://mosquitto.org/man/mosquitto_pub-1.html
  - https://mosquitto.org/man/mosquitto_sub-1.html
  - https://mosquitto.org/man/mosquitto_ctrl-1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: avoid repeating connection and credential options.

Each client reads a default config file: `$XDG_CONFIG_HOME/mosquitto_pub` or `$HOME/.config/mosquitto_pub` on POSIX, `%USERPROFILE%\mosquitto_pub` on Windows; likewise `mosquitto_sub` and `mosquitto_ctrl`. For snap installs the pub file is under `$HOME/snap/mosquitto/current/.config/`.

Format: one option per line as `-option value`; lines starting with `#` are comments.

```
# /path/to/.config/mosquitto_pub
-h broker.example.com
-u alice
-P PASSWORD
--cafile /path/to/ca.crt
```

Rules:
- Options given on the command line override the same options in the file, except message type options, of which only one can be specified.
- Some options cannot be negated, e.g. `-S`. TLS options can be negated with `--no-tls`.
- `-o config-file` (from version 2.1 for pub and sub) loads a specified file; when used, the default file is not loaded.

The page suggests config files are primarily for authentication, so you can authenticate without showing the username and password on the command line.

mosquitto_ctrl uses the same convention; its Dynamic Security page shows `--cafile`, `--cert`, `--key`, `-u admin` and `-h` in an options file.

## Checked

2026-11-03. Claims, option names, defaults and version notes were compared with the Mosquitto manual pages in `sources` (mosquitto(8), mosquitto.conf(5), mosquitto_pub, mosquitto_sub, mosquitto_rr, mosquitto_ctrl, and the Dynamic Security page where relevant). Nothing removed.

Method: documentation only; no commands were run.
