---
id: computing-software.database-administration.patroni.patroni-reinitialize-replica
name: patroni-reinitialize-replica
category: computing-software
field: database-administration
product: patroni
tags: [patroni, reinit, replica, basebackup, patronictl]
level: practitioner
status: docs-checked
description: "Rebuild a replica's data directory with patronictl reinit or POST /reinitialize."
sources:
  - https://patroni.readthedocs.io/en/latest/patronictl.html
  - https://patroni.readthedocs.io/en/latest/rest_api.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: recover a broken replica by re-cloning it.

```
patronictl reinit CLUSTER [MEMBER...] [--wait] [--force] [--from-leader]
```

- Rebuilds the Postgres standby managed by the named replica member(s). With no members it does nothing.
- `--wait` waits until reinitialization finishes.
- `--force` skips confirmation prompts.
- `--from-leader` gets the basebackup directly from the leader.

REST: `POST /reinitialize` reinitializes the data directory on the receiving node. It is allowed only on replicas. It removes the data directory and starts pg_basebackup or an alternative replica creation method.

The call may fail if Patroni is in a loop trying to recover (restart) a failed Postgres; set `{"force":true}` in the body to override. Set `{"from-leader":true}` to take the base backup directly from the leader, useful when running reinit while all replicas have failed.

The `/reinitialize` endpoint is what `patronictl reinit` calls.

## Checked

2026-11-08. Confirmed against the Patroni patronictl page (reinit synopsis and parameters) and REST API page (reinitialize endpoint). Removed the paragraph on `remove_data_directory_on_rewind_failure`, `remove_data_directory_on_diverged_timelines` and `use_pg_rewind` prerequisites, which neither page covers.

Method: documentation only; no commands were run.
