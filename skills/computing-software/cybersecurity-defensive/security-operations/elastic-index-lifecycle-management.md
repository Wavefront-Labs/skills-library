---
id: computing-software.cybersecurity-defensive.security-operations.elastic-index-lifecycle-management
name: elastic-index-lifecycle-management
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [elastic-security, index-lifecycle-management, ilm, data-tiers, data-streams, retention, searchable-snapshots, rollover]
level: practitioner
status: docs-checked
description: "Set retention for Elastic Security data with ILM: rollover, hot-warm-cold-frozen tiers, searchable snapshots, delete phase, and fixing stuck policies."
sources: ["https://www.elastic.co/guide/en/elasticsearch/reference/current/index-lifecycle-management.html", "https://www.elastic.co/guide/en/elasticsearch/reference/current/data-tiers.html", "https://www.elastic.co/guide/en/elasticsearch/reference/current/searchable-snapshots.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Index lifecycle management and retention

**Goal:** keep security data searchable for as long as investigations and policy need,
at the lowest storage cost, without manual index cleanup.

## Policy design
Decide per data type: how long hot (fast, recent investigations), how long searchable at
all (incident lookback), and the regulatory minimum.
```
PUT _ilm/policy/security-logs
{
  "policy": {"phases": {
    "hot":    {"actions": {"rollover": {"max_primary_shard_size": "50gb", "max_age": "1d"}}},
    "warm":   {"min_age": "7d",  "actions": {"forcemerge": {"max_num_segments": 1}}},
    "cold":   {"min_age": "30d", "actions": {"searchable_snapshot": {"snapshot_repository": "s3-repo"}}},
    "frozen": {"min_age": "90d", "actions": {"searchable_snapshot": {"snapshot_repository": "s3-repo"}}},
    "delete": {"min_age": "400d", "actions": {"delete": {}}}
  }}
}
```
## Attach to data streams
Set the `index.lifecycle.name` index setting to your policy in the index template (or a
component template) that creates the data stream:
```
PUT _component_template/security-logs-settings
{"template": {"settings": {"index.lifecycle.name": "security-logs"}}}
```
For Elastic Agent integration data streams, follow the Fleet documentation for overriding
their lifecycle policy.

## Tiers
Nodes carry the roles `data_hot`, `data_warm`, `data_cold` and `data_frozen`. The frozen tier
uses a shared cache to search snapshots held in the repository.

## Troubleshooting
```
GET logs-*/_ilm/explain?only_errors=true
POST <index>/_ilm/retry
```

## Gotchas
- Deleting by ILM is permanent; keep snapshots of anything you must retain.
- Detection rules and ML jobs looking back further than hot tier will be slower.
- Too many small shards hurt the cluster: roll over on size, not only on time.

## Verify
`GET logs-*/_ilm/explain` shows every security index in the expected phase with no errors; total
retention matches policy (oldest index date versus delete `min_age`).

## Checked
2026-10-28 Confirmed on the Elastic ILM pages (rollover, forcemerge, searchable snapshot, delete, explain, retry, put policy) and the data tiers and searchable snapshots pages: `max_primary_shard_size`, `max_age`, `max_num_segments`, `snapshot_repository`, `min_age`, `index.lifecycle.name`, `only_errors`, `_ilm/retry`, the four data tier roles, and the frozen-tier shared cache. Removed: the `@custom` component template claim and managed-policy advice, the list of common errors, the 12-months lookback figure and the SLM backup claim (not on the fetched pages).
Method: documentation only; no commands were run.
