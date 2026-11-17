---
id: computing-software.database-administration.scylladb.kb-stop-running-repair
name: kb-stop-running-repair
category: computing-software
field: database-administration
product: scylladb
tags: [repair, force-terminate-repair, rest-api, scylla-manager]
level: practitioner
status: docs-checked
description: "Stop a running ScyllaDB nodetool repair: POST /storage_service/force_terminate_repair on port 10000, active_repair check, why abort is not immediate, sctool for Manager repairs."
sources: ["https://github.com/scylladb/scylladb/blob/master/docs/kb/stop-local-repair.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Stopping a running repair

Aborting a repair started with `nodetool repair` is not instant. Use the REST API on the node (port 10000):

```
curl -X POST 'http://localhost:10000/storage_service/force_terminate_repair'
```
Check status:

```
curl -X GET 'http://localhost:10000/storage_service/active_repair/'
[1]
```
In the docs example this still returned `[1]` right after the abort, i.e. the repair still looked active.

The abort only sets a flag. The repair checks it at the start of each step (for example while negotiating sync boundaries or fetching missing rows), and each step can take a while, so an immediate check may still show the repair as RUNNING. Wait and check again; only if the aborted repair stays RUNNING forever, force the stop with the same POST.

If you use ScyllaDB Manager for repairs, stop them with its `sctool` command instead: a simple stop command via sctool already implements all the logic needed to stop a repair gracefully.

## Checked

2026-11-04. Confirmed against kb/stop-local-repair.rst: both REST calls on port 10000, abort flag, step names, wait before forcing, sctool for Manager repairs. Note the page uses the same force_terminate_repair POST both for the first abort and for the forced stop. Reworded the active_repair reading to match the page example.

Method: documentation only; no commands were run.
