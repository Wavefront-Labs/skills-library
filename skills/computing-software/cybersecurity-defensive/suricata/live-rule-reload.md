---
id: computing-software.cybersecurity-defensive.suricata.live-rule-reload
name: live-rule-reload
category: computing-software
field: cybersecurity-defensive
product: suricata
tags: [rule-reload, sigusr2, ruleset-reload, detection-engine-swap]
level: practitioner
status: docs-checked
description: "Reload rules without stopping Suricata via SIGUSR2, suricatasc reload-rules or ruleset-reload-nonblocking, and know what gets reloaded."
sources: ["https://docs.suricata.io/en/latest/rule-management/rule-reload.html", "https://docs.suricata.io/en/latest/unix-socket.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Live rule reload

- Signal: `kill -USR2 $(pidof suricata)`.
- Blocking: `suricatasc -c reload-rules` (alias of `ruleset-reload-rules`).
- Non-blocking: `suricatasc -c ruleset-reload-nonblocking`.
- Windows service: `sc.exe control Suricata 128` (non-blocking, results only in logs).
- `ruleset-reload-time`, `ruleset-stats`, `ruleset-failed-rules` report on the last reload.

## Reloaded
`vars` and `rule-files` from the YAML and `--include` files (unless `-S` was used), classification.config, reference.config, threshold.config, datasets used by rules, and per-tenant rule config.

## Process
New config and variables load, rule files load, a new detection engine is built and swapped in, threads update, then the old engine is freed. Packets keep flowing but memory use temporarily rises as two engines exist.

## Checked

2026-11-08. Read in full the raw Suricata user guide source for rule reload (doc/userguide/rule-management/rule-reload.rst) and the command list of unix-socket.rst (reload-rules alias, ruleset-reload-*, ruleset-reload-time, ruleset-stats, ruleset-failed-rules). Partial read: the rest of unix-socket.rst was not read. Nothing removed.

Method: documentation only; no commands were run.
