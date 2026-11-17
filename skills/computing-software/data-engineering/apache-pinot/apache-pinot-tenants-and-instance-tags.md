---
id: computing-software.data-engineering.apache-pinot.apache-pinot-tenants-and-instance-tags
name: apache-pinot-tenants-and-instance-tags
category: computing-software
field: data-engineering
product: apache-pinot
tags: [apache-pinot, tenant, tags, default-tenant, cluster-tenant-isolation-enable, updatetags, addtenant, broker-tenant, server-tenant]
level: practitioner
status: docs-checked
description: "Tenant model for isolating brokers and servers: _BROKER, _OFFLINE, _REALTIME tags, table tenants block, AddTenant, retagging."
sources: ["https://github.com/pinot-contrib/pinot-docs/blob/latest/basics/components/cluster/tenant.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tenants and instance tags

A tenant is a logical namespace (a text tag) that restricts where the cluster processes a table's queries. Tables with a tenant tag are stored and queried only on brokers and servers carrying the same tag. By default all tables, brokers and servers belong to `DefaultTenant`. If you plan several tenants, consider `cluster.tenant.isolation.enable=false` so new servers and brokers are not automatically tagged with DefaultTenant (the page states no default for this key).

A table picks tenants in its config:
```
"tenants": { "broker": "brokerTenantName", "server": "serverTenantName" }
```
Meaning: brokers tagged `brokerTenantName_BROKER` serve the table; offline segments live on servers tagged `serverTenantName_OFFLINE`; real-time segments (consuming and completed) live on servers tagged `serverTenantName_REALTIME`.

Create a tenant: `POST /tenants` tags **currently untagged** instances (already-tagged ones are not reassigned). Body fields:
- `tenantRole` (`BROKER` or `SERVER`), `tenantName`, `numberOfInstances`: required. If `numberOfInstances` is omitted it defaults to 0 and server creation fails.
- `offlineInstances`, `realtimeInstances`: required for server tenants; how many servers get the `_OFFLINE` and `_REALTIME` tags.
- Each of `offlineInstances` and `realtimeInstances` must be <= `numberOfInstances`; if their sum exceeds it, servers are co-located and one server gets both tags. Creation needs at least `numberOfInstances` untagged online instances.

CLI equivalent for a server tenant (`-instanceCount` is required for every AddTenant call; for SERVER also the two counts, note the capital T in `-realTimeInstanceCount`):
```
bin/pinot-admin.sh AddTenant -name sampleServerTenant -role SERVER -instanceCount 2 -offlineInstanceCount 1 -realTimeInstanceCount 1 -exec
```
Broker tenant: `-name sampleBrokerTenant -role BROKER -instanceCount 3 -exec`.

Servers that are already tagged (for example `DefaultTenant_OFFLINE`): update tags directly instead:
```
PUT /instances/<instance-name>/updateTags?tags=sampleServerTenant_OFFLINE,sampleServerTenant_REALTIME
```
A server may hold several tags. To grow or shrink an existing tenant use `PUT /tenants` with the same payload shape.

## Checked

2026-11-08. Read the whole pinot-docs tenant page. Confirmed tag suffixes, the tenants block, POST /tenants fields and validation, AddTenant flags, updateTags and PUT /tenants. Corrected `cluster.tenant.isolation.enable` (the page recommends setting it to false for multi-tenant clusters and states no default; the skill claimed default false) and removed the rebalance-after-retag gotcha, which the page does not state.

Method: documentation only; no commands were run.
