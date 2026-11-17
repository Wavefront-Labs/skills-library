---
id: computing-software.database-administration.couchdb.weatherreport-diagnostics
name: weatherreport-diagnostics
category: computing-software
field: database-administration
product: couchdb
tags: [weatherreport, diagnostics, troubleshooting, cluster-health, couchdb-3]
level: practitioner
status: docs-checked
description: "Diagnose a CouchDB 3 node or cluster with the weatherreport escript: options, the list of checks, severity levels, and running single checks."
sources:
  - https://raw.githubusercontent.com/apache/couchdb/main/src/docs/src/cluster/troubleshooting.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
WeatherReport diagnoses common problems on a CouchDB 3 node or cluster. Version 4 or later is not supported.

```
weatherreport --etc /path/to/etc
```

Options: `-c/--etc` path to the config directory, `-d/--level` minimum severity (default `notice`), `-l/--list` describe checks, `-e/--expert` more detailed diagnostics, `-h/--help`, and optional `check_name` arguments.

Severity names, most to least verbose: debug, info, notice, warning, error, critical, alert, emergency.

Checks listed by `--list`: custodian (shard safety/liveness), disk, internal_replication, ioq, mem3_sync, membership, memory_use, message_queues, node_stats, nodes_connected, process_calls, process_memory, safe_to_rebuild, search, tcp_queues.

Run specific checks by name:

```
weatherreport --etc /path/to/etc nodes_connected
```

Use `--level debug` for full detail of what each check does. A typical finding: a warning that a cluster member is not connected to this node and may be down.

## Checked

2026-11-04. Confirmed against the CouchDB cluster/troubleshooting page (WeatherReport): CouchDB 3 only, usage line and options, default level notice, severity order, the full --list check names, running named checks. Nothing removed.

Method: documentation only; no commands were run.
