---
id: computing-software.messaging-and-integration.debezium.mongodb-changestream-history-lost-recovery
name: mongodb-changestream-history-lost-recovery
category: computing-software
field: messaging-and-integration
product: debezium
tags: [mongodb, recovery, resume-token, snapshot]
level: advanced
status: docs-checked
description: "Recover a MongoDB connector failing with ChangeStreamHistoryLost or InvalidResumeToken after a long outage."
sources:
  - https://debezium.io/documentation/reference/stable/connectors/mongodb.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A connector stopped too long can fail with: `Command failed with error 286 (ChangeStreamHistoryLost): ... Resume of change stream was not possible, as the resume point may no longer be in the oplog`. It means the oplog no longer contains the connector's last offset, so it cannot resume.

With `snapshot.mode` of `initial` there is a mismatch: the offsets topic holds an offset, so no snapshot is attempted, yet the oplog lacks that position. The connector errors out.

Recovery options from the docs:

1. Delete the failed connector and create a new one with the same configuration but a different connector name. The new connector has no offsets, so it snapshots the current state and then streams.
2. Pause the connector, then remove its offsets or change the offset topic.

Prevention:

- Size the oplog (see mongodb-oplog-sizing-and-retention).
- Use heartbeats so the offset advances.
- Keep downtime shorter than the oplog window.

Other documented behaviours:

- If the connector task crashes, it restarts at the last recorded offset and may emit duplicates, so consumers must be idempotent. Offsets flush at the Connect `offset.flush.interval.ms`.
- If Kafka is unavailable, the connector waits and resumes.
- MongoDB can lose commits in certain failure situations, and the connector cannot capture changes MongoDB has lost.

## Checked

2026-11-08: read the Connector Unable to Start, Kafka Connect crashes, Kafka unavailable, stopped for a long interval and MongoDB loses writes sections, the offset flush note and the heartbeat.interval.ms property row of the Debezium MongoDB connector reference (raw AsciiDoc source of the cited page, connectors/mongodb.adoc). Confirmed the error text, both recovery options, the initial-mode mismatch and the documented behaviours. Removed: the re-emitted-as-snapshot gotcha and the snapshot-log Check line, which the page does not state.

Method: documentation only; no commands were run.
