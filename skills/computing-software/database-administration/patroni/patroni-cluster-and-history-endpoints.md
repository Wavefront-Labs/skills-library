---
id: computing-software.database-administration.patroni.patroni-cluster-and-history-endpoints
name: patroni-cluster-and-history-endpoints
category: computing-software
field: database-administration
product: patroni
tags: [patroni, rest-api, cluster-status, history, timelines]
level: practitioner
status: docs-checked
description: "Read cluster topology and failover history from GET /cluster and GET /history, and the patronictl equivalents."
sources:
  - https://patroni.readthedocs.io/en/latest/rest_api.html
  - https://patroni.readthedocs.io/en/latest/patronictl.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: inspect topology and past leader changes programmatically.

- `GET /cluster` returns JSON describing the current topology and state: a `members` list (name, role, state, `api_url`, host, port, timeline, tags, and for replicas receive and replay LSN and lag), the `scope`, and any `scheduled_switchover`.
- `GET /history` returns switchover/failover history in a format close to the timeline history files in `pg_wal`, plus a timestamp field with the creation time of the new timeline. Each entry holds timeline, LSN, reason and timestamp.

```
curl -s http://localhost:8008/cluster | jq .
curl -s http://localhost:8008/history | jq .
```

CLI counterparts:
- `patronictl history [CLUSTER] [-f pretty|tsv|json|yaml]` shows TL, LSN, Reason (from the Postgres .history file), Timestamp and New Leader. Default is pretty.
- `patronictl list [CLUSTER...] [-e] [-t] [-f FORMAT] [-W | -w SECONDS]` shows Cluster, Member, Host, Role (Leader, Standby Leader, Sync Standby, Replica), State (`running`, `streaming`, `in archive recovery`, `stopped`, `crashed`), TL, Receive/Replay LSN and lag in MB.
- `patronictl topology` shows members as a tree by replication connection.

## Checked

2026-11-08. Confirmed against the Patroni REST API page (cluster status endpoints) and the patronictl page (history, list and topology synopses and output columns). Removed the "since 4.1.0" note and the `max_timelines_history` sentence, which neither page states.

Method: documentation only; no commands were run.
