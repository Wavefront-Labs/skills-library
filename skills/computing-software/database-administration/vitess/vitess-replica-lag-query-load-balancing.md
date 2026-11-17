---
id: computing-software.database-administration.vitess.vitess-replica-lag-query-load-balancing
name: vitess-replica-lag-query-load-balancing
category: computing-software
field: database-administration
product: vitess
tags: [load-balancing, replication-lag, vtgate, healthy-degraded-unhealthy, min-number-serving-vttablets, discovery]
level: practitioner
status: docs-checked
description: "Tune how VTGate avoids lagging replicas: the three discovery flags, healthy, degraded and unhealthy states, matching vttablet thresholds, and the 3 second floor."
sources:
  - https://vitess.io/docs/25.0/user-guides/configuration-advanced/query-load-balancing/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
VTGate can keep read queries away from replicas whose replication lag is too high. A tablet is healthy (always gets queries), degraded (queries only if necessary) or unhealthy (no queries).

VTGate flags:
- `discovery_high_replication_lag_minimum_serving`: lag above this makes a tablet unhealthy; match vttablet's `unhealthy_threshold`.
- `discovery_low_replication_lag`: a tablet lagging beyond this is degraded and gets no queries, unless too many replicas exceed it, in which case the ones with least lag serve using a weighted average to exclude outliers; match vttablet's `degraded_threshold`.
- `min_number_serving_vttablets`: minimum tablets per replicating tablet type that keep being used even above the low threshold but below the high one.

Degraded tablets receive queries only when fewer than `min_number_serving_vttablets` non-degraded tablets exist in the same shard and tablet type. With only two replicas and the default of 2, only the unhealthy threshold applies; more replicas or a lower minimum are needed for other behaviour.

Recommended settings: `min_number_serving_vttablets` equal to the replicas needed for peak read traffic; the high threshold (with `unhealthy_threshold`) at the lag where an error is preferable to stale data; the low threshold (with `degraded_threshold`) at normal tolerable lag. A common use is a new replica restored from backup that starts far behind.

Gotchas: vtgate and vttablet flags can roll out separately but behaviour takes hold only when both are applied; do not set thresholds below 3 seconds because lag measurement is skewed there; the minimum is applied separately per tablet type (rdonly and replica); when lowering `discovery_low_replication_lag`, also lower vttablet `health_check_interval`, about half of it or less.

## Checked

2026-11-04. Flags, state semantics, recommendations and gotchas confirmed on the Query Load Balancing page.

Method: documentation only; no commands were run.
