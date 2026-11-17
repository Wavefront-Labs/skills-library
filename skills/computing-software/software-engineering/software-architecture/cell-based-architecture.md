---
id: computing-software.software-engineering.software-architecture.cell-based-architecture
name: cell-based-architecture
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, architecture-styles, cell-based-architecture, blast-radius, shuffle-sharding, cell-router]
level: advanced
status: draft
description: "Partition a system into independent cells with a thin routing layer to cap blast radius: cell sizing, partition keys, cell router, migration and deployment waves."
sources: ["https://docs.aws.amazon.com/wellarchitected/latest/reducing-scope-of-impact-with-cell-based-architecture/reducing-scope-of-impact-with-cell-based-architecture.html", "https://aws.amazon.com/builders-library/workload-isolation-using-shuffle-sharding/", "https://github.com/wso2/reference-architecture/blob/master/reference-architecture-cell-based.md"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cell-based architecture

**Idea:** run N complete, independent copies ("cells") of the stack, each serving a subset of
customers. A failure, bad deploy or poison request takes down one cell (1/N of users), not all.
Used by AWS services, Slack, DoorDash, Salesforce.

## Components
- **Cell**: full stack (compute, data stores, queues) with no synchronous dependency on other
  cells. Has a maximum size you've load-tested.
- **Partition key**: customer/tenant/account id (whatever most requests carry).
- **Cell router** (thinnest possible layer): maps key -> cell from a mapping table, cached
  aggressively; must be simpler and more reliable than anything behind it.
- **Control plane**: provisions cells, assigns new tenants, migrates tenants between cells.

## Design rules
- Cap cell size so it fits tested limits; add cells to scale out rather than growing cells.
- Avoid cross-cell calls; global data (catalogue, auth) is replicated read-only into each cell or
  served by a separate highly-available global service.
- **Deploy in waves**: one canary cell, then progressively more, with bake time and automatic
  rollback; a bad release hits one cell first.
- Shuffle sharding: give each tenant a random combination of cells/nodes so one noisy tenant's
  failure overlaps few others.
- Tenant migration tooling (copy data, dual-write or freeze, flip mapping) is needed from day one:
  for big tenants, rebalancing, and evacuating a sick cell.

## Costs
More infrastructure copies, operational tooling, harder cross-tenant queries (reporting needs an
aggregate data pipeline), and a router that must never be the single point of failure.

## Verify
Game day: kill or corrupt one cell; measure that only its tenants are affected and others' SLOs hold.
