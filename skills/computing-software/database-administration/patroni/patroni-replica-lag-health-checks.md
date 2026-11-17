---
id: computing-software.database-administration.patroni.patroni-replica-lag-health-checks
name: patroni-replica-lag-health-checks
category: computing-software
field: database-administration
product: patroni
tags: [patroni, rest-api, replication-lag, health-check, async]
level: practitioner
status: docs-checked
description: "Add a lag threshold to /replica and /async health checks using bytes or human-readable sizes."
sources:
  - https://patroni.readthedocs.io/en/latest/rest_api.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: keep lagging replicas out of read pools.

Append `lag=<max-lag>` to the replica or asynchronous endpoint:

```
GET /replica?lag=1048576
GET /replica?lag=1024kB
GET /replica?lag=10MB
GET /replica?lag=1GB
GET /async?lag=10MB
```

- The endpoint adds a latency check on top of the usual replica check and returns 200 only if lag is below the value.
- `max-lag` can be an integer in bytes or a human-readable value such as 16kB, 64MB, 1GB.
- For performance, the leader WAL position comes from the DCS key `cluster.last_leader_operation`, not a live query.
- Tag filters can be combined with the same query string: `GET /replica?lag=10MB&tag_key1=value1`.

`/replica` returns 200 only when the node is `running`, has the replica role and the `noloadbalance` tag is not set; otherwise 503.

For an alternative that returns ready/not-ready for Kubernetes, `GET /readiness?lag=<max-lag>&mode=apply|write` defaults the lag limit to `maximum_lag_on_failover`.

Related display data: `patronictl list` shows Receive LSN, Replay LSN and lag in MB per replica (added to the REST `/cluster` endpoint and CLI in 4.1.0), based on DCS contents refreshed roughly every `loop_wait` seconds.

## Checked

2026-11-03. Confirmed against the REST API page: `lag=` on `/replica` and `/async`, accepted units, the `cluster.last_leader_operation` source, tag filtering with the same query string and `noloadbalance` behaviour.

Method: documentation only; no commands were run.
