---
id: computing-software.database-administration.couchdb.stop-and-resume-resharding
name: stop-and-resume-resharding
category: computing-software
field: database-administration
product: couchdb
tags: [sharding, resharding, reshard-state, maintenance, shard-map]
level: advanced
status: docs-checked
description: "Pause all CouchDB resharding jobs with PUT /_reshard/state so external shard-map changes do not conflict, then resume from checkpoints."
sources:
  - https://raw.githubusercontent.com/apache/couchdb/main/src/docs/src/cluster/sharding.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Stopping resharding lets external tools or manual procedures that change the shard map avoid interfering with resharding jobs. Stop it before moving shards.

```
curl -s -H "Content-type: application/json" -XPUT $COUCH_URL:5984/_reshard/state \
  -d '{"state": "stopped", "reason":"Moving some shards"}'
{"ok": true}
```

The `reason` is optional. `GET /_reshard` then shows `"state": "stopped"` and your text in `state_reason`. If you find resharding stopped, read `state_reason` to see why someone stopped it.

Resume with the same `PUT` and `"state": "running"`. Shard splitting jobs continue from their last checkpoint.

## Checked

2026-11-04. Confirmed against the CouchDB cluster/sharding page (Stopping Resharding Jobs): PUT /_reshard/state with state and reason, state_reason in the summary, resume from last checkpoint. Nothing removed.

Method: documentation only; no commands were run.
