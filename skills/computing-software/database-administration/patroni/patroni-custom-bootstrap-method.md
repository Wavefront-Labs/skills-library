---
id: computing-software.database-administration.patroni.patroni-custom-bootstrap-method
name: patroni-custom-bootstrap-method
category: computing-software
field: database-administration
product: patroni
tags: [patroni, bootstrap, custom-script, recovery, pgbackrest]
level: advanced
status: docs-checked
description: "Replace initdb with a user script to bootstrap a cluster, including recovery_conf, no_params and keep_existing_recovery_conf."
sources:
  - https://patroni.readthedocs.io/en/latest/replica_bootstrap.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: bootstrap a new cluster from a backup or copy using a custom script.

```
bootstrap:
  method: my_method
  my_method:
    command: /path/to/script [param1]
    keep_existing_recovery_conf: False
    no_params: False
    recovery_conf:
      recovery_target_action: promote
      recovery_target_timeline: latest
      restore_command: <restore command>
```

Rules:
- Each method needs at least a name and a `command`; the command may be an absolute path or relative to the patroni command location. A special `initdb` method triggers the default behaviour, and then `method` can be omitted.
- Patroni passes `--scope` (cluster name) and `--datadir` (data directory) unless `no_params` is true.
- Extra key/value pairs in the method section are passed as `--name=value` arguments.
- If the script returns 0, Patroni configures and starts the instance. If a step fails or the exit code is non-zero, Patroni cleans up and releases the initialize lock so another node can try.
- A `recovery_conf` block generates recovery settings before starting (recovery.conf, or Postgres configuration for PostgreSQL 12+). It should usually include a `recovery_target_*` parameter with `recovery_target_action: promote`.
- `keep_existing_recovery_conf: True` keeps existing recovery.conf (PostgreSQL <= 11) or recovery.signal/standby.signal files and recovery settings (12+). This suits backup tools such as pgBackRest that generate recovery configuration.

Bootstrap methods are neither chained nor do they fall back to initdb if the chosen one fails. Patroni calls bootstrap only on the first node that takes the initialize key lock, when no initialize key exists in the DCS.

## Checked

2026-11-08. Confirmed against the Patroni "Replica imaging and bootstrap" page (read in full, bootstrap section). Added the initdb method and initialize-lock facts from the same page.

Method: documentation only; no commands were run.
