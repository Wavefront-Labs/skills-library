---
id: computing-software.cloud-infrastructure-engineering.azure.resource-graph-kql-joins-summarize-and-mv-expand
name: resource-graph-kql-joins-summarize-and-mv-expand
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, resource-graph, arg-kql, arg-joins, resource-graph-queries, mv-expand, az-graph-query, inventory]
level: practitioner
status: docs-checked
description: "Write Azure Resource Graph KQL: tables, supported joins, mv-expand on properties arrays, summarize for inventory, pagination past 1,000 rows and throttling."
sources: ["https://learn.microsoft.com/azure/governance/resource-graph/concepts/query-language", "https://learn.microsoft.com/azure/governance/resource-graph/samples/advanced", "https://learn.microsoft.com/azure/governance/resource-graph/concepts/work-with-data", "https://learn.microsoft.com/azure/governance/resource-graph/reference/supported-tables-resources"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Resource Graph KQL: joins, summarize, mv-expand

**Goal:** answer estate-wide questions (VM network details, resource counts per subscription)
across every subscription.

## Tables
`resources`, `resourcecontainers` (subscriptions, RGs, MGs), `advisorresources`, `policyresources`,
`securityresources`, `healthresources`, `recoveryservicesresources`, `networkresources`,
`authorizationresources` (role assignments), `resourcechanges`, `patchassessmentresources`.

## Supported KQL subset
`where, project, extend, summarize, count, top, order by, take/limit, distinct, mv-expand, join, union, parse, extract, todynamic, tostring, bag_keys`.
Limits: max **3 join or union operations** (counted together) and **3 mv-expand** per query; `join` kinds `innerunique, inner, leftouter, fullouter`;
mv-expand `RowLimit` default 128, max 2,000. You can request higher join and mv-expand limits through Help + support.

## Patterns
```kusto
// VMs with their NIC private IPs (mv-expand + join)
resources | where type =~ 'microsoft.compute/virtualmachines'
| mv-expand nic = properties.networkProfile.networkInterfaces
| extend nicId = tolower(tostring(nic.id))
| join kind=leftouter (
    resources | where type =~ 'microsoft.network/networkinterfaces'
    | mv-expand ipc = properties.ipConfigurations
    | project nicId = tolower(id), privateIp = tostring(ipc.properties.privateIPAddress)) on nicId
| project vm = name, resourceGroup, privateIp
```
```kusto
// Resource count by type and subscription name
resources | summarize n = count() by type, subscriptionId
| join kind=inner (resourcecontainers | where type == 'microsoft.resources/subscriptions' | project subscriptionId, subName = name) on subscriptionId
| project subName, type, n | order by n desc
```

## Running
```bash
az graph query -q "<kql>" --first 1000 --management-groups <mg>   # needs `resource-graph` extension
az graph query -q "<kql>" --skip-token <token>                     # page beyond 1000
```
By default a query returns at most 1,000 records (`--first` maximum 1000). Always `tolower()` IDs before
joining so casing differences do not break the match.

## Gotchas
- Results reflect your RBAC; a "missing" resource may just be unreadable.
- `properties` fields are dynamic — cast with `tostring()`/`toint()` before comparing or summarizing.
- Throttling is per user: for example at most 15 queries in a 5-second window, and the quota is subject to change (see the response headers `x-ms-user-quota-remaining` and `x-ms-user-quota-resets-after`).

## Verify
- [ ] Query count matches a portal blade count for a known subscription.
- [ ] Saved as a shared query or workbook for reuse.

## Checked
2026-10-31. Confirmed on Microsoft Learn (Resource Graph query language, work with data, advanced samples, overview and troubleshooting pages, `az graph` reference): join kinds, three join/union and three mv-expand limits, mv-expand RowLimit default 128 and max 2,000, 1,000-record default, `--skip-token` and `--management-groups`, extension requirement, 15 queries per 5 seconds throttle example. Corrected: join and union limits are counted together; mv-expand maximum is 2,000, not 400. Removed: the unattached-disk and unprotected-VM queries (property names not in the docs fetched), data-freshness and power-state claims, PowerShell paging line, advice to batch with union.
Method: documentation only; no commands were run.
