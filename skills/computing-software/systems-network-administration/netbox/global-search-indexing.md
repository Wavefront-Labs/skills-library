---
id: computing-software.systems-network-administration.netbox.global-search-indexing
name: global-search-indexing
category: computing-software
field: systems-network-administration
product: netbox
tags: [global-search, search-index, reindex]
level: practitioner
status: docs-checked
description: "Configure search weights and rebuild the index when needed."
sources: ["https://netboxlabs.com/docs/netbox/features/search/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Global search

Goal: find objects across the whole data model.

NetBox indexes relevant fields on each model by precedence so the most relevant results appear first. When searching the user can choose a lookup type such as exact or partial match; for partial matches the matching portion of the field is shown in the result.

**Custom fields** are included in search results only if configured with a search weight. Plugins can register their own models for inclusion with core models.

**Deferred indexing.** To avoid one background job per change, index updates are coalesced: changes committed over a short interval are buffered and applied together by a single background job. The pending buffer lives in the tasks Redis database. If that data is lost, recent updates may be discarded.

**Repair.** Rebuild the index from the database with the `reindex` management command:

```
manage.py reindex
```

**Failures.** A buffered batch that repeatedly fails (for example a persistent database error) is retried by a safety-net job a limited number of times and then discarded, with the failure logged at error level.

**Checklist**

1. Give useful custom fields a search weight.
2. Keep the worker running.
3. Run `reindex` after Redis loss.

## Checked

Method: docs-checked 2026-11-09 against https://netboxlabs.com/docs/netbox/features/search/ (downloaded; read the indexing, deferred update, Redis buffer, safety-net and reindex passages). Dropped the unconfirmed `python3 netbox/` prefix and the claim that apps or models can be passed to reindex.
