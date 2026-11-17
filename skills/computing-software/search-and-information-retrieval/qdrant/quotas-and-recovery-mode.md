---
id: computing-software.search-and-information-retrieval.qdrant.quotas-and-recovery-mode
name: quotas-and-recovery-mode
category: computing-software
field: search-and-information-retrieval
product: qdrant
tags: [quotas, disk-usage, http-507]
level: advanced
status: docs-checked
description: "Set memory and disk quotas (v1.19) that stop a full node taking writes with HTTP 507, and monitor them."
sources:
  - "https://qdrant.tech/documentation/ops-configuration/quotas/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Resource quotas (available as of v1.19.0) make a node reject updates that would consume more memory or disk once a limit is reached. They are disabled by default.

Configure per node under `storage.quotas` (or `QDRANT__STORAGE__QUOTAS__ENABLED=true` and `QDRANT__STORAGE__QUOTAS__MAX_DISK_USAGE_PERCENT=90`), or cluster-wide with `PUT /quotas?wait=true`, which propagates to every peer and persists:

```http
PUT /quotas?wait=true
{ "enabled": true, "max_disk_usage_percent": 90 }
```

Parameters: `enabled` (default false), `max_resident_memory_percent` and `max_disk_usage_percent` (1 to 100, unset means no quota; memory is measured against the cgroup limit if there is one, otherwise total system memory), and `release_margin_percent` (0 to 100, default 5).

Precedence: once a quota is set through the API, the config file is no longer read, and a node joining such a cluster takes the API configuration through consensus. Each node resolves its own quota and Qdrant does not warn when they differ, so use `PUT /quotas` for uniform limits.

When exceeded:

- Reads are never affected. A node over its limit still accepts and coordinates updates, but a shard replica on it is excluded and marked dead until it has room; the update succeeds if at least `write_consistency_factor` replicas accept it (default 1).
- Clients get HTTP 507 or gRPC `ResourceExhausted` only when no replica can accept the write, naming the resource, utilisation and limit.
- Deleting points is always allowed; deleting a vector or payload key is not, because it rewrites the point; shard transfers are always allowed.
- A limit trips on reaching it and clears only after usage falls `release_margin_percent` points below. At 90 with the default margin, writes stop at 90 percent and resume below 85. Changing the quota configuration clears any tripped limit.

Monitoring: `GET /quotas` returns this node's `config` and `usage` plus a `peers` map with each peer's usage and `exceeded` flag (a non-answering peer is omitted, itself a warning sign). The `/metrics` series `quota_exceeded{resource="memory"}` and `{resource="disk"}` stay at 1 until usage is under the margin, and `/telemetry` has a top-level `quota` field.

## Checked

Method: docs-checked 2026-11-09 against the Qdrant resource quotas page (landing_page repo, ops-configuration/quotas.md), read in full. The page has no recovery-mode content, so the recovery mode section, its environment variables and the alerting advice were removed; description and tags trimmed to match.
