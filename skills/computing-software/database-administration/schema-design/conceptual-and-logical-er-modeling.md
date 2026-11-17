---
id: computing-software.database-administration.schema-design.conceptual-and-logical-er-modeling
name: conceptual-and-logical-er-modeling
category: computing-software
field: database-administration
product: schema-design
tags: [database-administration, schema-design, er-diagram, data-modeling, conceptual-model, logical-model, keys-normalisation]
level: practitioner
status: draft
description: "Run conceptual, logical and physical data modeling: entities, relationships, cardinality and optionality in ER diagrams, then map to tables, keys and constraints."
sources:
  - https://www.oreilly.com/library/view/database-design-for/9780136788133/
  - https://dbml.dbdiagram.io/docs/
  - https://mermaid.js.org/syntax/entityRelationshipDiagram.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Conceptual and logical ER modeling

## Three levels
| Level | Audience | Contents |
|---|---|---|
| Conceptual | Business stakeholders | Entities, relationships, key business rules; no attributes beyond identifiers |
| Logical | Analysts, designers | All attributes, keys, cardinality/optionality, normalised to 3NF; DBMS-independent |
| Physical | DBAs, developers | Tables, types, indexes, partitions, constraints for a specific engine |

## Running the conceptual session (Hernandez-style)
1. Interview users; collect nouns (candidate entities) and verbs (relationships) from forms, reports, and process descriptions.
2. For each relationship ask two questions both ways: "Can a customer have more than one order?" (cardinality) and "Must every order have a customer?" (optionality).
3. Record business rules as you go ("an order needs at least one line", "a product may be discontinued but stays on old invoices").

## Notation (crow's foot)
```mermaid
erDiagram
  CUSTOMER ||--o{ ORDER : places
  ORDER ||--|{ ORDER_LINE : contains
  PRODUCT ||--o{ ORDER_LINE : "appears in"
```
`||` exactly one, `o|` zero or one, `|{` one or many, `o{` zero or many.

## Logical model steps
- Attributes per entity, each atomic (1NF); identify candidate keys.
- Resolve many-to-many into associative entities (ORDER_LINE).
- Normalise to 3NF; record deliberate denormalisation as a physical decision later.
- Attribute specifications: domain, allowed values, nullability, default, source.
- Subtypes/supertypes (party → person/organisation): choose single table, table per type, or table per concrete class at physical level.

## Physical mapping
- Entity → table; identifier → PK (surrogate or natural) + UNIQUE alternates.
- Relationship 1:N → FK on the N side with NOT NULL if mandatory; 1:1 → FK with UNIQUE; M:N → junction table.
- Business rules → CHECK, FK actions, triggers, or application logic (documented).

## Tooling
Diagram as code keeps models versioned: DBML (dbdiagram.io), Mermaid `erDiagram`, PlantUML; reverse-engineer existing databases with SchemaSpy, DBeaver ER diagrams, `pg_dump -s` into dbdiagram imports.

## Verify
Walk the diagram with business users using concrete examples (one real customer's orders); every report requirement can be answered by a query path through the model.
