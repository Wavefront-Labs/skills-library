---
id: computing-software.cloud-infrastructure-engineering.thanos.receive-shuffle-sharding
name: receive-shuffle-sharding
category: computing-software
field: cloud-infrastructure-engineering
product: thanos
tags: [thanos-receive, shuffle-sharding, shard-size, zone-awareness]
level: sme
status: docs-checked
description: "Give each tenant a stable subset of nodes in a ketama hashring using shuffle_sharding_config."
sources: ["https://thanos.io/tip/components/receive.md/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Receive shuffle sharding

Shuffle sharding gives a tenant a subset of the hashring, approximating a single-tenant experience in a multi-tenant system. It works only with ketama.

```json
[{
  "endpoints": [
    {"address": "node-1:10901", "az": "foo"},
    {"address": "node-2:10901", "az": "bar"}
  ],
  "algorithm": "ketama",
  "shuffle_sharding_config": {
    "shard_size": 2,
    "cache_size": 100,
    "overrides": [
      {"shard_size": 3, "tenants": ["prefix-tenant-*"], "tenant_matcher_type": "glob"}
    ]
  }
}]
```

This sets a default shard size of 2 and 3 for tenants starting with `prefix-tenant-`.

- `cache_size`: size of the in-memory LRU cache of computed subrings. It is bounded because an attacker could spam random tenants.
- With zones, `shard_size / number_of_azs` nodes are chosen per zone, so each tenant gets a unique, consistent set.
- `zone_awareness_disabled` ignores AZs; then set shard size to `max(nodes_in_any_az, replication_factor)`.

Only stateless shuffle sharding is supported; Receive does not store or check shard overlaps.

## Checked

2026-11-03. Confirmed against the Thanos Receive page (components/receive.md) and the Thanos troubleshooting page (operating/troubleshooting.md): hashrings and ketama, shuffle sharding, tenancy and decommissioning, quorum formula, Cap'n Proto, limits and gates, defaults, out-of-bound and out-of-order causes. Added the documented fixes and the out-of-order window flag warnings. Removed: closing 'Verify' tips and other statements the page does not state.

Method: documentation only; no commands were run.
