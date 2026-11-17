---
id: computing-software.networking-hardware-and-wireless.juniper-junos.cli-modes
name: cli-modes
category: computing-software
field: networking-hardware-and-wireless
product: juniper-junos
tags: [juniper-junos, cli-modes, operational-mode, configuration-mode, junos-cli]
level: practitioner
status: draft
description: "Move between Junos operational and configuration mode and run operational commands from inside configuration mode with run."
sources: ["https://www.juniper.net/documentation/", "https://www.juniper.net/documentation/us/en/software/junos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Operational vs configuration mode
Goal: know which prompt you are in and how to issue commands without switching modes.

Junos has two modes. Operational mode (`user@host>`) is for show, ping, request and clear. Configuration mode (`user@host#`) edits the candidate configuration.

```
user@host> configure
Entering configuration mode
[edit]
user@host# run show interfaces terse | match ge-0/0/0
user@host# exit
user@host> show configuration | display set | match ntp
```

- `configure exclusive` locks the candidate so nobody else can edit; `configure private` gives you a private copy of the candidate (only your changes are committed).
- `run <cmd>` executes any operational command without leaving the hierarchy.
- Use `?` for context help and Space or Tab for completion; `show | display set` prints set-format lines you can paste elsewhere.

Gotcha: plain `configure` is shared. Two admins editing at once get `warning: uncommitted changes will be lost` or commit each other's half-done edits. On shared boxes use `configure private` or `exclusive`.

## Verify
- Prompt ends in `#` after `configure` and `>` after `exit`.
- `show system users` lists other logged-in sessions before you start editing.
