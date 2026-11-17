---
id: computing-software.data-engineering.data-modelling.supertype-subtype-modelling
name: supertype-subtype-modelling
category: computing-software
field: data-engineering
product: data-modelling
tags: [data-modelling, supertype-subtype, entity-relationship, inheritance, table-per-type]
level: advanced
status: draft
description: "Model supertype/subtype entities (party, product variants, payment methods) and choose single-table, table-per-subtype or table-per-concrete-type physical designs."
sources:
  - https://www.dama.org/cpages/body-of-knowledge
  - https://books.google.com/books?vid=ISBN9780471380238
  - https://martinfowler.com/eaaCatalog/classTableInheritance.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Supertype and subtype modelling

**Goal:** represent entities that share common attributes but differ in specifics (Person/Organisation as Party; Card/BankTransfer as PaymentMethod) without null-riddled tables or duplicated logic.

## Logical model
- **Supertype** holds shared attributes and the identifier (`party_id`, `party_type`).
- **Subtypes** hold specific attributes and share the supertype key.
- Decide: **exclusive** (a party is a person XOR an organisation) vs **overlapping**; **complete** (every supertype row has a subtype) vs incomplete.

## Physical options
| Pattern | Tables | Pros | Cons |
|---|---|---|---|
| Single table (roll-up) | `party` with all columns + `party_type` | simple queries, one join | many nullable columns, weak constraints |
| Table per subtype (class table) | `party` + `person` + `organisation` keyed by `party_id` | clean constraints, shared FK target | joins for full picture |
| Table per concrete type (roll-down) | `person`, `organisation`, each with common columns | no joins per type | cross-type queries need UNION, no single FK target |

## Table-per-subtype in SQL
```sql
CREATE TABLE party (party_id BIGINT PRIMARY KEY, party_type CHAR(1) NOT NULL CHECK (party_type IN ('P','O')),
                    created_at TIMESTAMP NOT NULL);
CREATE TABLE person (party_id BIGINT PRIMARY KEY REFERENCES party, party_type CHAR(1) NOT NULL DEFAULT 'P' CHECK (party_type = 'P'),
                     first_name TEXT, last_name TEXT, birth_date DATE,
                     FOREIGN KEY (party_id, party_type) REFERENCES party (party_id, party_type));
```
The `(party_id, party_type)` composite FK (needs a UNIQUE on those columns in `party`) enforces exclusivity in OLTP databases.

## In analytics models
- Dimensions usually **roll up** into one wide dimension (`dim_customer` with `customer_type` and nullable type-specific columns) because BI tools prefer one table.
- Facts that apply only to one subtype can join to a subtype-specific dimension.
- Semi-structured option: common columns + a VARIANT/JSON column for type-specific attributes when subtypes are many and volatile.

## Gotchas
- Too many subtypes with few attributes each: use single table or JSON.
- Changing type (a lead becomes a customer) is a state change, not a subtype change; model it as status/role, not inheritance.

## Verify
Every supertype row has exactly one subtype row (for exclusive, complete hierarchies): `count(*)` per type matches.
