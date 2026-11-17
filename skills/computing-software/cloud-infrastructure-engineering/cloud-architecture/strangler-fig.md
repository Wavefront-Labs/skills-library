---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.strangler-fig
name: strangler-fig
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, modernisation, strangler-fig, incremental-migration, facade-routing, legacy-modernisation, feature-parity, traffic-shifting, decommissioning]
level: advanced
status: docs-checked
description: "Replace a legacy system incrementally with the strangler fig pattern: routing facade, slice selection, data sync, cutover with rollback, and retiring old parts."
sources: ["https://learn.microsoft.com/azure/architecture/patterns/strangler-fig", "https://martinfowler.com/bliki/StranglerFigApplication.html", "https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/strangler-fig.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Strangler fig incremental migration

Replace specific functionality with new services piece by piece behind a facade, until the legacy system has no dependants and can be decommissioned. Fowler's reasoning: a like-for-like rewrite usually fails because it takes long, users cannot wait for new features, existing behaviour is hard to pin down, and much of it is unwanted.

## Steps
1. **Put a facade (proxy) in front** of the legacy system between clients and both systems. Initially it routes everything (or most requests) to legacy. In the AWS guidance new features are built as services rather than added to the monolith, while bugs are still fixed in the monolith; routing can be by API URL.
2. **Find seams and slices.** Break the problem into parts, extracting individual business needs into components. AWS suggests DDD and event storming when the domain is unclear (premature decomposition can get boundaries wrong); look for classes with few dependencies and own data access.
3. **Replace slice by slice**, shifting requests at the facade each iteration. Structure new pieces so they too can later be intercepted and replaced.
4. **Cross-system calls**: use an anti-corruption layer adapter between old and new so legacy callers reach migrated services without large code changes and the new design is not forced into legacy conventions. In the AWS example it is a class inside the monolith (such as a `UserServiceFacade`) that is removed when all dependants are migrated. If legacy code is unmodifiable and database-centric, Azure notes the database can send messages to new services (a trigger, or change data capture reading the transaction log).
5. **Data (the hard part)**. Azure's example for splitting a shared database: new service reads and writes the monolithic database for its domain; then an isolated domain database is loaded by ETL and kept in sync by change data capture while legacy keeps working; validate consistency; cut over so the domain database is the system of record; then remove the domain's tables and procedures from the monolith. Rollback is possible in the sync phase and at the start of cutover; after legacy objects are removed it means restoring them and replaying changes, so treat removal as a deliberate final step. AWS alternative: the microservice owns its data and a queue plus synchronising agent updates the monolith database, which is eventually consistent and best treated as tactical.
6. **Retire**: when everything is migrated, decommission the legacy system. Then remove the facade, or keep it as an adapter for legacy clients.

## Preconditions and when not to use
- You must be able to intercept requests to the back end, and be able to modify the legacy system (or have another integration point such as its database). AWS adds code-base access to its prerequisites.
- Not suited to small systems that are simple to replace, or when the original must be fully decommissioned quickly.
- Benefit is largest for big, risky monoliths where users must keep getting new features.

## Gotchas
- The facade must keep up with the migration and must not become a single point of failure or bottleneck; with synchronous calls between services consider circuit breakers (AWS).
- Services and data stores used by both systems must be accessible to both at once.
- The facade and ACL are transitional architecture: Fowler argues reduced risk and earlier value outweigh their cost.
- Organisational change matters too: without it the new system can end up as rigid as the old (Fowler, citing Conway's Law).

## Verify
- [ ] The facade can route each migrated slice back to legacy, and that rollback has been exercised.
- [ ] The system of record for each data domain is written down at every stage.
- [ ] Remaining legacy surface area is tracked and has a decommission date.

Related: computing-software.cloud-infrastructure-engineering.cloud-architecture.anti-corruption-layer, computing-software.cloud-infrastructure-engineering.cloud-architecture.migration-strategy-lift-and-shift-vs-replatform

## Checked
2026-11-08, documentation only.
Confirmed against: Azure Architecture Center, Strangler Fig pattern (last updated 2026-06-02); Martin Fowler, Strangler Fig (2024); AWS Prescriptive Guidance, Strangler fig pattern.
Removed as unconfirmed: Debezium and DMS as named tools, weighted and cohort routing and shadow-mode comparison, the "zero traffic for an agreed period" retirement rule, and the saga advice.
Method: documentation only; no commands were run.
