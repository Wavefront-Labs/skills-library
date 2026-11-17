---
id: computing-software.cybersecurity-defensive.falco.rule-priority-levels
name: rule-priority-levels
category: computing-software
field: cybersecurity-defensive
product: falco
tags: [priority, severity, warning, notice, debug]
level: intro
status: docs-checked
description: "Pick a Falco rule priority from EMERGENCY to DEBUG, using the project guidelines, and know that priority does not control evaluation order."
sources:
  - https://falco.org/docs/concepts/rules/basic-elements/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The `priority` field of a Falco rule is a severity, like syslog severity, and it appears in text and JSON output. It does not override other rules and does not set evaluation order. Order comes from the sequence in which rules are defined and loaded.

Valid values, case-insensitive: `emergency`, `alert`, `critical`, `error`, `warning`, `notice`, `informational`, `debug`.

Guidelines used for the default ruleset:
- Writing state (filesystem and similar): `ERROR`.
- Unauthorized read of state (reading sensitive files): `WARNING`.
- Unexpected behaviour (an unexpected shell in a container, an unexpected network connection): `NOTICE`.
- Behaviour against good practice (unexpected privileged containers, containers with sensitive mounts, interactive commands as root): `INFO` (the documented valid value is spelled `informational`).
- Exception: the false-positive-prone rule Run shell untrusted is `DEBUG`.

Choose the priority by the damage a true positive would indicate, not by how often the rule fires.

Gotcha: do not try to make one rule beat another by raising its priority; to change which rule runs, change the order of definitions or use the override mechanisms.

## Checked

2026-11-08. Read the cited basic-elements page in full and corrected statements that went beyond it.

Method: documentation only; no commands were run.
