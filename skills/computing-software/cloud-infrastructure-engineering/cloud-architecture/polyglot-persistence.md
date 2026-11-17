---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.polyglot-persistence
name: polyglot-persistence
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, database-selection, polyglot-persistence, data-store-per-service, change-data-capture, data-consistency]
level: advanced
status: docs-checked
description: "Apply polyglot persistence: pick a store per access pattern, know when to combine models, and weigh the operational and consistency cost of many engines."
sources: ["https://martinfowler.com/bliki/PolyglotPersistence.html", "https://learn.microsoft.com/azure/architecture/guide/technology-choices/data-store-overview", "https://debezium.io/documentation/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Polyglot persistence

Fowler's definition: an enterprise has a variety of storage technologies for different kinds of data,
asking first how the data will be manipulated and only then which technology fits.

## When to combine models (Azure data store guide)
Use more than one model when:
- access patterns diverge (point lookup versus wide analytical scan versus full-text relevance);
- life cycle and retention differ (immutable raw versus curated structured);
- latency and throughput requirements conflict.

Avoid premature fragmentation: use one service while it still meets performance, scale and governance
objectives, and avoid duplicate transformation pipelines across stores unless necessary.

## Steps
1. **One authoritative store per kind of data.** Azure's antipattern list includes a search index
   becoming the primary data store.
2. **Choose a store per access pattern** only when it is a strategic need. Fowler: utility projects do not
   gain enough to justify a new technology; the drivers are reduced development drag or intensive data
   needs, and even then many projects are better off relational.
3. **Keep derived stores in sync** from the authoritative store. Debezium, for example, captures changes
   from MySQL, PostgreSQL, Oracle and MongoDB and writes them onward through sink connectors. Prefer
   change capture or events over application dual writes.
4. **State the consistency contract.** Fowler notes clustered NoSQL stores raise new questions about
   consistency and availability, and the single transactional source of truth no longer holds sway.
5. **Limit the zoo.** Each store adds an interface to learn, and Fowler stresses that data storage is
   usually a performance bottleneck, so you must understand how the technology works. Azure warns
   against adding a model without operational maturity such as monitoring and backups.

## Gotchas
- Fowler: a component boundary is a good way to wrap a storage technology chosen for how its data is used.
- Azure: multiple microservices sharing one database creates coupling.

## Verify
- [ ] Each kind of data names its authoritative store and why any second model is needed.
- [ ] Each additional engine has backup, monitoring and an owner.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed: Fowler's polyglot persistence article (cost in complexity, strategic versus utility projects,
consistency and availability questions) and the Azure sections "Combine models and avoid pitfalls" and
the antipattern list; Debezium's documentation landing page (supported source databases, sink connectors).
Removed as unconfirmed on those pages: the transactional outbox, DMS, "rebuildability" and lag-contract
rules, and the named OpenSearch/Redis example stack.
