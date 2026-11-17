---
id: computing-software.database-administration.mongodb.read-preference-and-tag-sets
name: read-preference-and-tag-sets
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, replica-set, read-preference, secondary-preferred, nearest, tag-sets, maxstalenessseconds, hedged-reads, analytics-nodes]
level: practitioner
status: docs-checked
description: "Route MongoDB reads with read preference modes, tag sets and maxStalenessSeconds, and understand the stale-read and failover consequences of reading secondaries."
sources:
  - https://www.mongodb.com/docs/manual/core/read-preference/
  - https://www.mongodb.com/docs/manual/core/read-preference-tags/
  - https://www.mongodb.com/docs/manual/core/read-preference-staleness/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Read preference

**Goal:** offload the right reads to secondaries without serving dangerously stale data.

## Modes
| Mode | Reads from |
|---|---|
| `primary` (default) | Primary only; errors if none |
| `primaryPreferred` | Primary, secondary if no primary |
| `secondary` | Secondaries only |
| `secondaryPreferred` | Secondaries, primary if none |
| `nearest` | Any eligible member within the latency window (`localThresholdMS`), primary or secondary |

In mongosh use `cursor.readPref()` or `Mongo.setReadPref()`; drivers take the mode, `maxStalenessSeconds` and tag sets as connection options or per operation (see the driver documentation).

## Tag sets for workload isolation
Tag the replica set members in the replica set configuration, then pass tag set lists with the read preference. Tag sets are tried in order; once one matches, the remaining sets are ignored. An empty document `{ }` as the last element means "any eligible member" and avoids an error when nothing matches.

## maxStalenessSeconds
Minimum 90 seconds (a smaller value raises an error). Secondaries whose estimated lag is greater than the value are excluded.

## What reading secondaries costs
- Eventual consistency: a user may not see their own write. Use `primary` for read-after-write paths, or causally consistent sessions.
- While there is no primary, `primary` reads fail and `secondary` reads can continue.
- Secondaries carry the same write load; offloading reads does not create more capacity if they are also near saturation. Losing a member then overloads the rest.


## Verify
Run the report and confirm from the secondary's own metrics or logs that it served the reads and the primary did not.

## Checked

2026-10-28. Confirmed against MongoDB manual read preference pages: mode behaviour (primary default, primaryPreferred, nearest within the latency window, localThresholdMS), tag set order and the empty document fallback, maxStalenessSeconds minimum of 90 seconds, causal consistency with majority read and write concern, transactions with reads must use primary. Removed unconfirmed: the 15 ms default, connection string example, rs.reconfig tag example, Atlas ANALYTICS tag, hedged reads version range, orphaned-document note, election time, opcounters check.

Method: documentation only; no commands were run.
