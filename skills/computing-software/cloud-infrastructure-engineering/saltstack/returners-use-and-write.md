---
id: computing-software.cloud-infrastructure-engineering.saltstack.returners-use-and-write
name: returners-use-and-write
category: computing-software
field: cloud-infrastructure-engineering
product: saltstack
tags: [saltstack, returners, return, custom-returner, file-roots, virtual]
level: practitioner
status: docs-checked
description: "Send Salt command results to external systems with --return, and write a custom returner module with returner(ret) in _returners."
sources:
  - https://raw.githubusercontent.com/saltstack/salt/master/doc/ref/returners/index.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Returners

Returners ship minion command results to external systems (Redis, MongoDB, MySQL, ...) in addition to the master. Their configuration comes from the minions and is generally read once at load time.

Use: add `--return <name>`; comma-separate names for several.

Write one:
- A Python module with at least `returner(ret)`, receiving a dict of the job's return data.
- Put it in `_returners/` under `file_roots` and sync it to the master or minion. A custom returner with a built-in's name replaces the built-in.
- The name defaults to the filename; `__virtual__` can override it.

## Checked

2026-11-09. Read against the returners source (doc/ref/returners/index.rst); --return usage, the returner function, _returners placement, replacement of built-ins and naming were confirmed there. Nothing removed.
Method: documentation only; no commands were run.
