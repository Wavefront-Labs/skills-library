---
id: computing-software.software-engineering.software-architecture.context-mapping-and-anti-corruption-layer
name: context-mapping-and-anti-corruption-layer
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, domain-driven-design, ddd, context-mapping, anti-corruption-layer, bounded-context, strategic-design]
level: practitioner
status: verified
description: "Map bounded-context relationships (customer-supplier, conformist, shared kernel, open host) and build an anti-corruption layer for legacy or external models."
sources:
  - https://github.com/ddd-crew/context-mapping
  - https://learn.microsoft.com/en-us/azure/architecture/patterns/anti-corruption-layer
  - https://www.domainlanguage.com/ddd/reference/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Context mapping and the anti-corruption layer

## Context map
A diagram of bounded contexts and the relationships between the teams and models that own them. Draw it as-is first (reality, including mess), then to-be.

## Relationship patterns (Evans, Domain-Driven Design)
Partnership, Shared Kernel, Customer-Supplier, Conformist, Anticorruption Layer, Open Host Service and Published Language are listed on contextmapper.org's context map page; the free 2015 DDD Reference PDF text contains Partnership, Customer/Supplier, Conformist and Anticorruption Layer but none of the other names. Confirm Separate Ways and Big Ball of Mud (marked below) in the book; this skill did not find them in a free source.

| Pattern | Meaning | Use when |
|---|---|---|
| Partnership | two teams succeed or fail together, coordinate closely | mutually dependent contexts, aligned teams |
| Shared Kernel | a small shared subset of model/code | very close teams; keep it tiny and jointly owned |
| Customer-Supplier (U/D) | upstream plans with downstream's needs | downstream has negotiating power |
| Conformist | downstream adopts upstream's model as is | upstream will not change; its model is acceptable |
| Anti-Corruption Layer (ACL) | downstream translates upstream's model into its own | upstream model is poor, legacy or foreign |
| Open Host Service | upstream offers a well-defined protocol for many consumers | many downstreams |
| Published Language | a documented exchange format (schema, events) | integration across contexts/companies |
| Separate Ways (confirm in the book) | no integration; duplicate instead | integration costs more than it gives |
| Big Ball of Mud (confirm in the book) | boundary around a messy area | mark it and protect others from it |
Label edges with U (upstream) / D (downstream). Context Mapper DSL (contextmapper.org) can model and generate diagrams.

## Anti-corruption layer
A translation layer that keeps the foreign model out of your domain.
```python
class LegacyCrmCustomerAdapter:          # implements our domain port
    def __init__(self, client: LegacyCrmClient): self.client = client
    def get_customer(self, customer_id: CustomerId) -> Customer:
        raw = self.client.fetch_cust(str(customer_id))          # CUST_NM, CUST_STAT_CD="A"...
        return Customer(
            id=customer_id,
            name=raw["CUST_NM"].strip().title(),
            status=CustomerStatus.ACTIVE if raw["CUST_STAT_CD"] == "A" else CustomerStatus.INACTIVE,
        )
```
Components: facade over the foreign API, adapters implementing domain ports, translators mapping data and errors, and sometimes a separate service if several contexts need the same translation.

## Rules
- Foreign types never appear in domain code (enforce with architecture tests).
- Translate errors and codes too (legacy status codes into domain exceptions).
- The ACL is the natural place for caching, retries, and circuit breakers around the upstream.
- During strangler-fig migrations the ACL lets the new system run beside the legacy one.

## Verify
- [ ] Context map reviewed with every team on it; U/D directions agreed.
- [ ] Domain module has no imports from upstream client/DTO packages.
