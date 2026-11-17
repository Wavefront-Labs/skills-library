---
id: computing-software.database-administration.pgbackrest.monitoring-with-info-json
name: monitoring-with-info-json
category: computing-software
field: database-administration
product: pgbackrest
tags: [pgbackrest, monitoring, info, json, jq]
level: advanced
status: docs-checked
description: "Check last backup time and last archived WAL by reading info JSON with jq or from inside PostgreSQL."
sources:
  - https://pgbackrest.org/user-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: alert when backups or archiving stop.

The JSON from `info` lists every backup for each stanza plus WAL archive information, so it suits any monitoring tool.

With jq (the guide says this syntax requires v1.5), last successful backup stop time and last archived WAL:

```
pgbackrest --output=json --stanza=demo info | jq '.[0] | .backup[-1] | .timestamp.stop'
pgbackrest --output=json --stanza=demo info | jq '.[0] | .archive[-1] | .max'
```

The first returns epoch seconds. jq may round large numbers such as system identifiers, so test queries carefully.

Inside PostgreSQL, the guide wraps the command in a function that uses `COPY ... FROM PROGRAM` to load `pgbackrest --output=json info` into a temp table and cast the text to `jsonb`. A query can then take the last element of the `backup` and `archive` arrays per stanza, convert `timestamp.stop` with `to_timestamp`, and report `max` as the last archived WAL.

Alert if the last backup stop time is older than your schedule allows or if the WAL max stops advancing. `info` also reports `backup/expire running` while those commands run.

## Checked

2026-11-08: the jq queries, the COPY FROM PROGRAM function, to_timestamp conversion and the jq rounding note confirmed in the User Guide Monitoring section. Changed: jq version wording now matches the guide. Partial reads: the User Guide, Command Reference and Configuration pages are long, so only the sections relevant to this skill were read, not every page end to end.

Method: documentation only; no commands were run.
