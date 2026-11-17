---
id: computing-software.messaging-and-integration.debezium.mongodb-oplog-sizing-and-retention
name: mongodb-oplog-sizing-and-retention
category: computing-software
field: messaging-and-integration
product: debezium
tags: [mongodb, oplog, retention, capacity]
level: advanced
status: docs-checked
description: "Size the MongoDB oplog or set a minimum retention window so Debezium can resume after downtime."
sources:
  - https://debezium.io/documentation/reference/stable/connectors/mongodb.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The oplog has a size limit, so older entries are cleared as it grows. If the connector's last position is overwritten while it is stopped, startup can fail with an invalid resume token error, depending on `snapshot.mode`.

Two approaches from the docs:

- Increase the oplog size to greater than the peak number of oplog entries per hour.
- On MongoDB 4.4 and later, increase the minimum number of hours an entry is retained. Entries from the last n hours are then guaranteed even if the oplog reaches its maximum. This is usually preferred, but for high-load clusters near capacity, set the maximum size.

Sizing formula:

```
oplog size = (Oplog GB/hour) x (average reaction time to a Debezium failure)
```

Example from the docs: growth of 3 GB per hour and two hours of downtime means a 6 GB oplog. With a 1 GB limit and 3 GB/hour growth, entries are cleared three times an hour and a failed connector's position is likely lost.

Monitor `Oplog GB/Hour` and `Replication Oplog Window`. If Debezium is offline longer than the replication oplog window while the oplog grows faster than it can be consumed, the connector will fail.

Pair with heartbeats: set `heartbeat.interval.ms` (default `0`) so offsets advance when only non-captured collections change.

Check: read the oplog window from your MongoDB monitoring and confirm it exceeds your recovery time.

## Checked

2026-11-03. Page used: the Debezium mongodb connector reference, https://debezium.io/documentation/reference/stable/connectors/mongodb.html.
Confirmed against it: both approaches, MongoDB 4.4 retention hours, the sizing formula and the 3 GB per hour examples, the metrics to monitor, heartbeat.interval.ms.
Removed or reworded: the capped-collection wording and the graceful-stop gotcha.
Method: documentation only; no commands were run.
