---
id: computing-software.cloud-infrastructure-engineering.victoriametrics.victoriametrics-cluster-architecture-and-multitenancy
name: victoriametrics-cluster-architecture-and-multitenancy
category: computing-software
field: cloud-infrastructure-engineering
product: victoriametrics
tags: [cluster, vminsert, vmselect, vmstorage, multitenancy, account-id, shared-nothing]
level: advanced
status: docs-checked
description: "Understand vminsert, vmselect and vmstorage roles, ports, key flags and the tenant URL formats of cluster VictoriaMetrics."
sources: ["https://docs.victoriametrics.com/victoriametrics/cluster-victoriametrics/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Victoriametrics cluster architecture and multitenancy

Cluster VictoriaMetrics is a shared-nothing design.

- `vmstorage` stores raw data and returns data for a time range and label filters; nodes do not talk to each other.
- `vminsert` accepts writes and spreads them over vmstorage nodes with consistent hashing over the metric name and all labels.
- `vmselect` runs queries by fetching from all configured vmstorage nodes.

Ports: vminsert 8480 (path `/insert`), vmselect 8481 (path `/select`), vmstorage 8482 for HTTP, with RPC listeners `-vminsertAddr` (8400) and `-vmselectAddr`. Change HTTP with `-httpListenAddr`.

Key flags: `-storageNode=<host>` on vminsert and vmselect; `-retentionPeriod`, `-storageDataPath`, `-storage.minFreeDiskSpaceBytes` on vmstorage; `-storageNode.discoveryInterval` and `-storageNode.filter`; `-disableRerouting`; `-search.denyPartialResponse`; `-memory.allowedPercent`; `-search.maxMemoryPerQuery`.

Multitenancy URLs:
- Write: `http://<vminsert>:8480/insert/<accountID>[:projectID]/<suffix>`
- Read: `http://<vmselect>:8481/select/<accountID>/prometheus/<suffix>`
- Headers `AccountID` and `ProjectID` can replace the IDs in the path (`-enableMultitenancyViaHeaders`, on by default from v1.150.0).
- All tenants: `/insert/multitenant/<suffix>` and `/select/multitenant/<suffix>`, choosing tenants via the `vm_account_id` and `vm_project_id` labels.
- Tenant list: `/admin/tenants?start=...&end=...`.
- Series deletion: `/delete/<accountID>/prometheus/api/v1/admin/tsdb/delete_series?match[]=...`.

Query paths include `api/v1/query`, `query_range`, `series`, `labels`, `export`, `status/tsdb`; the UI is at `/select/<accountID>/vmui/`; Graphite at `/select/<accountID>/graphite/<suffix>`.

## Checked

2026-11-03. Flags, endpoints, HTTP paths, defaults, limits and version gates were checked against the official VictoriaMetrics documentation pages cited in `sources` (docs.victoriametrics.com, fetched this batch) with a phrase-by-phrase comparison. No wrong claims were found; no claims were removed.

Method: documentation only; no commands were run.
