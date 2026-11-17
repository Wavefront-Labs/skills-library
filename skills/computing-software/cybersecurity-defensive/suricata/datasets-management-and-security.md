---
id: computing-software.cybersecurity-defensive.suricata.datasets-management-and-security
name: datasets-management-and-security
category: computing-software
field: cybersecurity-defensive
product: suricata
tags: [dataset-add, dataset-reload, allow-write, dataset-paths]
level: advanced
status: docs-checked
description: "Manage datasets at runtime and safely: unix socket commands, reload behaviour, file path rules, allow-write and allow-absolute-filenames."
sources: ["https://docs.suricata.io/en/latest/rules/datasets.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Dataset runtime and security

## Unix socket commands
`dataset-add`, `dataset-remove`, `dataset-lookup` (each `<set name> <set type> <data>`), `dataset-clear <set name> <set type>`, `dataset-dump`, and `dataset-add-json <set name> <set type> <data> <json_info>`. Data is base64 for strings, hex for md5 and sha256. Changes apply immediately.

## Reloads
Dynamic sets (defined in YAML or using only `state` or `save`) are not reloaded. Static sets (only `load`) are re-read after a rule reload.

## Paths
- `load` is relative to the rule file; absolute and parent paths allowed.
- `save` and `state` are relative to the data directory under the local state dir (confirm with `suricata --build-info`) and reject absolute or `..` paths.

## Settings
- `datasets.rules.allow-absolute-filenames` (default false): enabling lets any rule overwrite any writable file Suricata can reach.
- `datasets.rules.allow-write` (default true): false makes rules using `save` or `state` fail to load.

## Checked

2026-11-08: read in full against the OISF/suricata doc/userguide rst source (rules/datasets) read in full; the claims, names, values and examples left in this skill match the page text. Shortened the description.

Method: documentation only; no commands were run.
