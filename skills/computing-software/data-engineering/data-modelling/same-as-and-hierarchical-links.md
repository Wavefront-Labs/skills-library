---
id: computing-software.data-engineering.data-modelling.same-as-and-hierarchical-links
name: same-as-and-hierarchical-links
category: computing-software
field: data-engineering
product: data-modelling
tags: [data-modelling, same-as-link, hierarchical-link, data-vault, deduplication]
level: sme
status: draft
description: "Model duplicates and hierarchies in Data Vault 2.0 with same-as links (SAL) and hierarchical links (HAL): structure, loading, and resolving them in business vault."
sources:
  - https://datavaultalliance.com/
  - https://books.google.com/books?vid=ISBN9780128025109
  - https://automate-dv.readthedocs.io/en/latest/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Same-as and hierarchical links

**Goal:** record that two hub keys represent the same real-world entity, or that one is the parent of another, without altering hubs.

## Same-as link (SAL)
Use when the same customer exists under different business keys (CRM id vs web id, duplicates within one source, master data merges).
```sql
create table sal_customer (
  sal_customer_hk   binary(32) primary key,          -- hash of (master_hk, duplicate_hk)
  customer_master_hk binary(32) not null,            -- hub_customer key considered the survivor
  customer_dup_hk    binary(32) not null,            -- hub_customer key being mapped
  load_date timestamp not null,
  record_source varchar not null
);
```
- Both columns reference the **same hub**.
- Fed by an MDM system, matching rules, or a source that records merges.
- Add an effectivity satellite on the SAL if mappings can be undone or change over time.

## Hierarchical link (HAL)
Parent-child relationships within one hub (org units, product hierarchy, bill of materials):
```sql
create table hal_org_unit (
  hal_org_unit_hk binary(32) primary key,
  org_unit_parent_hk binary(32) not null,
  org_unit_child_hk  binary(32) not null,
  load_date timestamp not null,
  record_source varchar not null
);
```
Track validity with an effectivity satellite (re-orgs move children).

## Using them downstream
- Business vault / information mart: resolve SAL to a survivor key (`coalesce(master_hk, hk)`) so facts from all duplicates roll up to one customer.
- Flatten HAL to a closure table or path columns (level_1..n) for BI.

## Gotchas
- Chains (A->B, B->C) must be resolved transitively; compute the root survivor recursively.
- Do not delete or rewrite hub rows to "merge" entities: the SAL is the audit trail.

## Verify
After resolution, counts of distinct survivor keys match the MDM golden record count; the hierarchy has no cycles (recursive query terminates).
