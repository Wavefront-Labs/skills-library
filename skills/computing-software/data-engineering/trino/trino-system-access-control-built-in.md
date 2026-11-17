---
id: computing-software.data-engineering.trino.trino-system-access-control-built-in
name: trino-system-access-control-built-in
category: computing-software
field: data-engineering
product: trino
tags: [system-access-control, access-control-properties, read-only, allow-all, access-control-config-files]
level: practitioner
status: docs-checked
description: "Choose and configure Trino system access control (default, allow-all, read-only, file, opa, ranger) and combine several, with the performance warning."
sources: ["https://github.com/trinodb/trino/blob/master/docs/src/main/sphinx/security/built-in-system-access-control.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Trino system access control built in

A system access control enforces authorization globally, before connector-level checks. Enable one by creating `etc/access-control.properties` on all cluster nodes, for example `access-control.name=allow-all`.

Available names:
- `default`: everything permitted except user impersonation and triggering graceful shutdown. Used when nothing is configured.
- `allow-all`: everything permitted.
- `read-only`: reads of data and metadata plus setting system or catalog session properties are allowed; writes such as `CREATE`, `INSERT`, `DELETE` are denied.
- `file`: rules from a config file.
- `opa`: Open Policy Agent.
- `ranger`: Apache Ranger policies.
Anything else requires a custom implementation of the system access control API.

Several systems at once: list their property files, comma-separated, in `access-control.config-files` (paths relative to the install path, or absolute) instead of the default file. Systems are checked until one denies; if none denies, access is granted. Example:

```properties
access-control.config-files=etc/file-based.properties,etc/ranger.properties
```

Warning from the docs: this is complex to maintain and every system and policy is evaluated for each query, which can hurt performance.

Access control must be configured on the coordinator. Operations performed on workers, such as graceful shutdown, need it configured on all workers too.

## Checked

2026-11-09. Pages read in full against this skill:
- https://github.com/trinodb/trino/blob/master/docs/src/main/sphinx/security/built-in-system-access-control.md

Confirmed (page read as raw markdown): access-control.properties setup, the six built-in names and behaviours, multiple systems via access-control.config-files, the performance warning and the coordinator/worker note.
Removed or reworded: nothing; every concrete claim matched the page.

Method: documentation only; no commands were run.
