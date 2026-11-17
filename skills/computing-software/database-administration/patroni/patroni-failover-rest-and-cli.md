---
id: computing-software.database-administration.patroni.patroni-failover-rest-and-cli
name: patroni-failover-rest-and-cli
category: computing-software
field: database-administration
product: patroni
tags: [patroni, failover, patronictl, rest-api, data-loss]
level: advanced
status: docs-checked
description: "Use POST /failover or patronictl failover for an unhealthy cluster, and compare it with switchover."
sources:
  - https://patroni.readthedocs.io/en/latest/rest_api.html
  - https://patroni.readthedocs.io/en/latest/patronictl.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: promote a chosen candidate when automatic failover cannot.

`/failover` is for when there are no healthy nodes, for example failing over to an asynchronous standby when no synchronous standby is healthy enough. A leader is not required to be absent; it can also run on a healthy cluster. The POST body requires `candidate`. If `leader` is also given, a switchover is triggered instead.

```
curl -s http://localhost:8008/failover -XPOST -d '{"candidate":"postgresql1"}'
```

CLI: `patronictl failover [CLUSTER] [--group N] --candidate NAME [--force]`. The docs recommend `switchover` for healthy clusters and warn that failover can lose data depending on how current the promoted replica is.

Comparison table:
- Leader must be specified: failover no, switchover yes.
- Candidate must be specified: failover yes, switchover no.
- Can run in pause: failover yes; switchover yes (only to a specific candidate).
- Can be scheduled: failover no; switchover yes (not in pause).

In a cluster without a leader, a manual failover candidate may promote even if it is not in `/sync` members (synchronous mode), its lag exceeds the maximum, or its timeline is older than the last known one.

## Checked

2026-11-08. Confirmed against the Patroni REST API page (switchover and failover endpoints, comparison table, healthy standby warning) and the patronictl page (failover synopsis and warning). `--group` takes a Citus group ID.

Method: documentation only; no commands were run.
