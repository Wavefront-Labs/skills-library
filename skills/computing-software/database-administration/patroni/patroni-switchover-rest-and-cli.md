---
id: computing-software.database-administration.patroni.patroni-switchover-rest-and-cli
name: patroni-switchover-rest-and-cli
category: computing-software
field: database-administration
product: patroni
tags: [patroni, switchover, patronictl, rest-api, scheduling]
level: practitioner
status: docs-checked
description: "Perform or schedule a planned switchover with POST /switchover or patronictl switchover."
sources:
  - https://patroni.readthedocs.io/en/latest/rest_api.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: move leadership in a healthy cluster.

`/switchover` works only when there is a leader. The POST body requires `leader`; `candidate` and `scheduled_at` are optional. Without a candidate, all eligible nodes participate in the leader race after the leader steps down.

```
curl -s http://localhost:8008/switchover -XPOST -d '{"leader":"postgresql1","candidate":"postgresql2"}'
curl -s http://localhost:8008/switchover -XPOST -d '{"leader":"postgresql0","scheduled_at":"2019-09-24T12:00+00"}'
```

Status codes: 200 done, 202 scheduled, 400/412/503 errors with details in the body. `DELETE /switchover` removes a scheduled switchover (used by `patronictl flush CLUSTER switchover`).

CLI:

```
patronictl switchover [CLUSTER] [--group N] [--leader|--primary NAME] --candidate NAME [--scheduled TIMESTAMP] [--force]
```

`--scheduled` takes an unambiguous timestamp, preferably with time zone, or the literal `now`. Scheduling is not possible in pause mode, and in pause a switchover works only to a specific candidate. With synchronous mode, the candidate must be among `/sync` members.

Designed for a healthy cluster: a leader exists and synchronous standbys are available. Otherwise use failover. `patronictl list` footer shows the scheduled switchover.

## Checked

2026-11-03. Confirmed against the REST API page (`/switchover` body keys, status codes, DELETE) and the patronictl page (switchover and flush options, scheduling).

Method: documentation only; no commands were run.
