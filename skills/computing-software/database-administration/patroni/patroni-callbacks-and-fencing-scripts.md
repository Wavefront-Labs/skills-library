---
id: computing-software.database-administration.patroni.patroni-callbacks-and-fencing-scripts
name: patroni-callbacks-and-fencing-scripts
category: computing-software
field: database-administration
product: patroni
tags: [patroni, callbacks, pre-promote, before-stop, fencing]
level: advanced
status: docs-checked
description: "Hook scripts in the postgresql section: on_start, on_role_change, pre_promote and before_stop semantics."
sources:
  - https://patroni.readthedocs.io/en/latest/yaml_configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: run scripts at lifecycle events with correct expectations.

```
postgresql:
  callbacks:
    on_start: /path/to/script
    on_stop: /path/to/script
    on_restart: /path/to/script
    on_reload: /path/to/script
    on_role_change: /path/to/script
  pre_promote: /path/to/fencing-script
  before_stop: /path/to/script
```

- Callbacks (`on_reload`, `on_restart`, `on_role_change`, `on_start`, `on_stop`) receive the action, role and cluster name. `on_restart` runs when Postgres restarts without changing role; `on_role_change` when promoted or demoted.
- `pre_promote` is a fencing script executed during failover after acquiring the leader lock but before promoting. If it exits non-zero, Patroni does not promote the replica and removes the leader key from DCS.
- `before_stop` runs immediately before stopping Postgres. Unlike callbacks it is synchronous and blocks shutdown until done, but its return code does not decide whether shutdown continues.
- `post_bootstrap` / `post_init` run after cluster initialization and get a connection string URL.

Example from tools integration: use `patroni_barman ... config-switch --barman-server NAME --barman-model MODEL` as the `on_role_change` callback so Barman streams from the new primary after a failover. It relies on `barman config-switch`, available since Barman 3.10.

## Checked

2026-11-03. Confirmed against YAML Configuration Settings (callbacks, pre_promote, before_stop, post_init) and Tools integration (Barman `config-switch` callback example).

Method: documentation only; no commands were run.
