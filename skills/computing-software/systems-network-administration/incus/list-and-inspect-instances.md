---
id: computing-software.systems-network-administration.incus.list-and-inspect-instances
name: list-and-inspect-instances
category: computing-software
field: systems-network-administration
product: incus
tags: [incus, list, info, filter, show-log, recursion, rest-api]
level: intro
status: docs-checked
description: "List and inspect Incus instances: incus list filters by type, status, location or regex, incus info --show-log, and the matching REST API queries."
sources:
  - https://raw.githubusercontent.com/lxc/incus/main/doc/howto/instances_manage.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# List and inspect instances

```
incus list
incus list type=container
incus list status=running
incus list location=server1
incus list debian.*
incus info <instance>
incus info <instance> --show-log
```

- `incus list` shows type, status and location (clusters).
- A bare argument is a regular expression on the name; `incus list --help` shows all filters.
- API: `GET /1.0/instances`; add `recursion=2` for detail, or `filter=name+eq+debian`.
- `incus info` details one instance; `--show-log` appends the latest log lines. API: `GET /1.0/instances/<name>`.

## Checked

2026-11-04: confirmed against the Incus manage-instances how-to (list filters, regular-expression name argument, `info --show-log`, API queries with recursion and filter). Nothing removed.

Method: documentation only; no commands were run.
