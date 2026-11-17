---
id: computing-software.search-and-information-retrieval.qdrant.tenant-principal-index
name: tenant-principal-index
category: computing-software
field: search-and-information-retrieval
product: qdrant
tags: [is-tenant, is-principal, tenant-index, multitenancy, idx-tenant]
level: advanced
status: docs-checked
description: "Mark a keyword index as the tenant key or a datetime/integer index as the principal index to optimise storage layout."
sources:
  - "https://qdrant.tech/documentation/manage-data/multitenancy/"
  - "https://qdrant.tech/documentation/manage-data/indexing/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Two payload index flags tell Qdrant how the data is queried.

Tenant index: for multitenant collections where every query filters by one tenant field.

```json
{ "field_name": "group_id",
  "field_schema": { "type": "keyword", "is_tenant": true } }
```

Qdrant uses it to co-locate the vectors of one tenant, so that a tenant's data can be read in one sequential pass instead of many random disk seeks. `is_tenant` is optional and available from v1.11.0.

Principal index: for a field that is the main ordering or range key, such as a timestamp.

```json
{ "field_name": "timestamp",
  "field_schema": { "type": "datetime", "is_principal": true } }
```

The docs use it to optimize storage for faster search when requests are primarily filtered by that field, for example time-based filters on timestamped data.

The multitenancy guide pairs a tenant keyword index with a single collection partitioned by payload.

## Checked

2026-11-03. Confirmed on the Qdrant multitenancy and indexing pages: `is_tenant` on a keyword index (v1.11.0, optional) and its co-location effect, `is_principal` and its purpose. Removed unconfirmed notes about a single tenant key, creation-time setting and nested indexes, and the recommendation claim.

Method: documentation only; no commands were run.
