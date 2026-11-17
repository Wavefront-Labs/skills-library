---
id: computing-software.search-and-information-retrieval.qdrant.multitenancy-approaches
name: multitenancy-approaches
category: computing-software
field: search-and-information-retrieval
product: qdrant
tags: [multitenancy, tenant, shard-key, payload-partitioning]
level: advanced
status: docs-checked
description: "Serve many tenants with payload partitioning, user-defined shards, tiered tenants with a fallback shard, or separate collections."
sources:
  - "https://qdrant.tech/documentation/production-operations/multitenant-search/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The docs say to choose from the number of tenants, their relative sizes and their isolation needs, starting with payload partitioning when many tenants share a collection configuration.

| Situation | Starting design | Trade-off |
| --- | --- | --- |
| Many small tenants, similar data and vector config | One collection with a tenant payload field and index | Tenants share resources and configuration |
| A few large tenants plus many small | Tiered multitenancy (shared and dedicated shards) | Plan shard capacity and promotion |
| A few tenants need different collection config or collection-level permissions | Separate collections | Each collection adds resource and operational overhead |
| A tenant's data must sit on specific nodes | Custom shard keys with explicit placement | You manage placement and capacity |

These can be combined, for example a custom shard holding several tenants separated by payload filters.

Details:

- Shared collection: add a tenant id such as `group_id` to every payload and create a keyword index on it with `is_tenant: true` (from v1.11) so tenant points are stored together. Include the tenant filter in every query, update and delete that selects by payload, and derive the tenant from the authenticated user rather than trusting the request. The index helps storage and search but does not authorise requests: a client with unrestricted credentials can omit the filter.
- If indexing is the bottleneck and every search is tenant-filtered, the per-tenant HNSW configuration sets `m: 0` to disable the global graph with a positive `payload_m` keeping payload-aware links; unfiltered queries then get slower.
- Dedicated shards: create the collection with user-defined sharding, create shard keys and send the shard key with reads and writes. A shard key picks where an operation runs, a payload filter picks which points match, so use both when a shard holds several tenants. On Qdrant Cloud disable automatic shard rebalancing before placing shards by hand. Avoid a dedicated shard per small tenant.
- Tiered multitenancy (from v1.16): small tenants share a fallback shard and a large tenant moves to a dedicated shard in the same collection. The tenant filter is still needed on the fallback shard. The sharding method cannot be changed in place, so choose custom sharding at creation, and the fallback shard must fit on one node.
- Separate collections suit a limited number of tenants with different vector schemas, settings or permissions; prefer a shared collection when tenants share a data model.
- Enforce access in an authenticated application or with restricted credentials such as granular access keys, keeping admin keys on trusted services, and test with attempts to omit or change the tenant id.

## Checked

Method: docs-checked 2026-11-09 against the Qdrant multitenancy design page (landing_page repo, deploy-and-scale/multitenant-search.md, which carries the cited URL as an alias), read in full. Removed the unconfirmed Cloud 1000-collection limit, the JWT-embedded-filter advice and the sharding_method JSON detail.
