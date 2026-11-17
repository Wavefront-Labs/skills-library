---
id: computing-software.networking-hardware-and-wireless.asterisk.cli-usage-and-configuration
name: cli-usage-and-configuration
category: computing-software
field: networking-hardware-and-wireless
product: asterisk
tags: [networking-hardware-and-wireless, asterisk, cli, cli-conf, cli-permissions, cli-aliases, help, core-show, core-stop, core-restart]
level: intro
status: docs-checked
description: "Use the Asterisk CLI: syntax and help, core show application or function, cli.conf, cli_permissions.conf, cli_aliases.conf, prompt variables, and core stop or restart."
sources:
  - https://docs.asterisk.org/Operation/Asterisk-Command-Line-Interface/CLI-Syntax-and-Help-Commands/
  - https://docs.asterisk.org/Configuration/Core-Configuration/Asterisk-CLI-Configuration/
  - https://docs.asterisk.org/Operation/Running-Asterisk/Stopping-and-Restarting-Asterisk-From-The-CLI/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CLI usage and configuration
Commands follow `<module name> <action type> <parameters>` (for example `voicemail show users`, `core set debug 5`). They exist only while the providing module is loaded. Tab completes commands and many arguments. `help` is an alias of `core show help`; `help core show` lists a prefix; `help core show version` gives usage. `core show application <name>` and `core show function <name>` describe dialplan items.

Config files:
- `cli.conf`: commands to run at startup.
- `cli_permissions.conf`: restrict or allow commands per user; read the sample carefully, mistakes can create security issues.
- `cli_aliases.conf`: aliases (via `res_clialiases.so`).
Commands: `cli check permissions`, `cli reload permissions`, `cli show permissions`, `cli show aliases`. The prompt comes from the `ASTERISK_PROMPT` environment variable set before starting Asterisk, with substitutions such as `%d` (date).

Stopping and restarting, each with three forms:
- `core stop now` / `core restart now`: immediate, ends calls.
- `core stop gracefully` / `core restart gracefully`: refuses new calls, waits for current calls.
- `core stop when convenient` / `core restart when convenient`: waits until idle but still accepts new calls.
- `core abort shutdown` cancels a pending graceful or when-convenient shutdown.

## Checked
2026-11-04: read the cited Asterisk documentation pages (CLI-Syntax-and-Help-Commands, Asterisk-CLI-Configuration, Stopping-and-Restarting-Asterisk-From-The-CLI) and confirmed the commands, options, defaults and names stated above. Nothing removed; every claim was confirmed.

Method: documentation only; no commands were run.
