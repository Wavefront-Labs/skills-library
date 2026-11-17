---
id: computing-software.data-engineering.data-modelling.entity-relationship-modelling
name: entity-relationship-modelling
category: computing-software
field: data-engineering
product: data-modelling
tags: [data-modelling, er-modelling, entity-relationship, conceptual-logical-physical, cardinality, optionality, crows-foot, associative-entity, subtype-supertype, dbml, dmbok]
level: practitioner
status: draft
description: "Build conceptual, logical and physical ER models: entities, attributes, keys, crow's foot cardinality and optionality, associative entities, subtypes, and DDL."
sources:
  - https://www.dama.org/cpages/body-of-knowledge
  - https://dbml.dbdiagram.io/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Entity-relationship modelling (conceptual, logical, physical)

**Goal:** a shared, precise picture of the business's things and rules, refined into a database design that enforces them. DMBOK's Data Modeling and Design knowledge area frames three levels.

## The three levels
| Level | Contains | Audience |
|---|---|---|
| Conceptual | Main entities and relationships, named in business language; no attributes or keys beyond essentials | Business stakeholders |
| Logical | All attributes, primary/alternate keys, relationships with cardinality, normalised (typically 3NF), technology-independent | Analysts, architects |
| Physical | Tables, columns, data types, indexes, partitioning, constraints for a specific DBMS; may denormalise for performance | Engineers, DBAs |

## Elements and notation (crow's foot)
- **Entity**: a thing the business tracks (Customer, Order). Test: does it have instances you can count and identify?
- **Attribute**: a fact about an entity (order_date). Atomic, one value per instance.
- **Identifier/key**: natural key (business id) and, physically, a surrogate key.
- **Relationship** with **cardinality** (one / many) and **optionality** (zero allowed or mandatory) at each end:
  - `Customer ||--o{ Order`: each order has exactly one customer; a customer has zero or many orders.
  - Read both directions aloud as sentences and confirm them with the business; most modelling errors are cardinality errors.
- **Associative entity** resolves many-to-many (Student-Course -> Enrollment, with its own attributes like grade).
- **Subtype/supertype**: Party -> Person | Organisation; decide exclusive vs overlapping, complete vs incomplete; physically implement as single table + type column, table per subtype, or both.

## Process
1. Gather nouns and rules from processes, documents, existing systems.
2. Draft conceptual model; walk through real scenarios ("a customer changes address mid-order").
3. Logical: attributes, keys, normalise; record rules that can't be drawn (e.g. "end_date > start_date").
4. Physical: types, constraints (PK, FK, UNIQUE, CHECK, NOT NULL), indexes for access paths.

## Diagrams as code
```dbml
Table customers { customer_id bigint [pk]  email varchar [unique, not null] }
Table orders { order_id bigint [pk]  customer_id bigint [not null, ref: > customers.customer_id]  ordered_at timestamp }
```
DBML/dbdiagram, Mermaid `erDiagram`, or modelling tools (ER/Studio, erwin, SqlDBM) keep diagrams versioned; generate DDL from the physical model.

## Verify
- [ ] Each relationship read as two sentences has been confirmed by a business owner.
- [ ] Every many-to-many is resolved in the logical model.
- [ ] Physical DDL enforces the stated cardinalities with FKs/NOT NULL where the platform supports them.
