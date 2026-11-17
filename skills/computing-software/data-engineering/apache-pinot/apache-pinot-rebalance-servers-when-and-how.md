---
id: computing-software.data-engineering.apache-pinot.apache-pinot-rebalance-servers-when-and-how
name: apache-pinot-rebalance-servers-when-and-how
category: computing-software
field: data-engineering
product: apache-pinot
tags: [apache-pinot, rebalance, capacity-change, replication, replicasperpartition, reassigninstances, updatetags, queries-disable, pinot-set-instance-id-to-hostname, tenant-migration]
level: practitioner
status: docs-checked
description: "When a Pinot table rebalance is required, how to change tags and replication, migrate tenants, and stop query routing to a server."
sources: ["https://github.com/pinot-contrib/pinot-docs/blob/latest/operate-pinot/rebalance/README.md", "https://github.com/pinot-contrib/pinot-docs/blob/latest/operate-pinot/rebalance/rebalance-servers/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rebalancing servers

Rebalance recomputes segment-to-server assignment. It is not a single command but a series of steps. It is needed after:
1. capacity changes (adding, removing or replacing servers),
2. increasing or decreasing replication,
3. changing segment assignment (for example to replica-group),
4. moving a table to another tenant.

Brokers have their own rebalance, and when a server is tagged or untagged to a tenant every table of that tenant needs rebalancing.

Steps for common cases:
- Replication: update `replication` (OFFLINE) or `replicasPerPartition` (REALTIME) in the table config, then rebalance.
- Retag servers (0.6.0 and later): `PUT /instances/{instanceName}/updateTags?tags=<comma separated tags>`, for example `a_OFFLINE,a_REALTIME`. A server defaults to `DefaultTenant_OFFLINE` and `DefaultTenant_REALTIME`.
- Tenant migration: change `tenants` and any `tagPoolConfig.tag` in both the realtime and offline table configs, then call the rebalance API with `reassignInstances=true`.
- Keep host names consistent while resizing the cluster with `pinot.set.instance.id.to.hostname=true`.

Stop new queries reaching a server before you retag, replace or troubleshoot it, without leaving the cluster:
```
PUT /instances/Server_10.1.10.51_7000/state?state=QUERIES_DISABLE
PUT /instances/Server_10.1.10.51_7000/state?state=QUERIES_ENABLE
```
This sets the server's `queriesDisabled` flag so brokers stop routing new queries; the Helix participant stays online and already routed queries continue. It applies to server instances only.

Gotcha: for the older `PUT /instances/{instanceName}` update (0.5.0 and prior, which `updateTags` replaced), the GET output and PUT input differ because the name `Server_host_port` is split into separate `host` and `port` fields.

## Checked

2026-11-09. Read the Pinot docs rebalance overview and the full opening sections of the rebalance-servers page (changes that require a rebalance, tags, QUERIES_DISABLE, replication, tenant migration, and the `reassignInstances` explanations). Confirmed all statements above. Corrected: the payload mismatch gotcha belongs to the old instance PUT API, not `updateTags`. Not read: the dry-run, pre-checks, downtime and bootstrap option sections of the rebalance-servers page.
Method: documentation only; no commands were run.
