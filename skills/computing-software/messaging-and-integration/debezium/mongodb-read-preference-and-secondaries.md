---
id: computing-software.messaging-and-integration.debezium.mongodb-read-preference-and-secondaries
name: mongodb-read-preference-and-secondaries
category: computing-software
field: messaging-and-integration
product: debezium
tags: [mongodb, read-preference, secondary, latency]
level: advanced
status: docs-checked
description: "Stream MongoDB changes from a secondary with readPreference in the connection string and understand the latency and election behaviour."
sources:
  - https://debezium.io/documentation/reference/stable/connectors/mongodb.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default the connector reads from the primary, which gives the lowest latency. Set the MongoDB `readPreference` parameter in `mongodb.connection.string` to read elsewhere:

```json
"mongodb.connection.string": "mongodb://mongo1:27017,mongo2:27017/?replicaSet=rs0&readPreference=secondaryPreferred"
```

Setting `readPreference=secondaryPreferred` makes the connector read from a secondary. Events from a secondary can arrive later because of resource contention or network latency, and because change streams only emit after a change is majority committed: a secondary can emit only after it learns that a majority of voting members wrote it to their journals.

Election behaviour:

- When the connection string names a replica set and does not set `directConnection=true`, the connector periodically checks that the serving member still satisfies the read preference. The interval is `mongodb.heartbeat.frequency.ms`, so role changes are not detected instantly and events may keep arriving from the old member briefly.
- If the member no longer qualifies, the connector closes the stream and resumes from the last processed offset on an eligible member.
- For the exact `primary` and `secondary` modes with no eligible member, consumption waits while the task stays running.
- `primaryPreferred` and `secondaryPreferred` use the driver fallback.

On sharded clusters `mongos` applies the preference to each shard's members.

Gotcha: unavailable members trigger reconnects with exponential backoff and streaming resumes from the last captured event.

Check: compare event timestamps against writes during peak load.

## Checked

2026-11-03. Page used: the Debezium mongodb connector reference, https://debezium.io/documentation/reference/stable/connectors/mongodb.html.
Confirmed against it: default of reading the primary, readPreference in mongodb.connection.string, majority-commit latency, mongodb.heartbeat.frequency.ms checks, election behaviour, mongos, exponential backoff.
Removed or reworded: the claim that secondaryPreferred reduces primary load.
Method: documentation only; no commands were run.
