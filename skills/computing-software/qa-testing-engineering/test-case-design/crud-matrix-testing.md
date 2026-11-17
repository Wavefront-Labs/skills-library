---
id: computing-software.qa-testing-engineering.test-case-design.crud-matrix-testing
name: crud-matrix-testing
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [crud-matrix, crud-testing, data-lifecycle, functional-completeness, istqb-ta]
level: practitioner
status: docs-checked
description: "Build a CRUD matrix of entities versus functions to find untested create/read/update/delete paths, orphaned data and missing permission checks."
sources:
  - https://en.wikipedia.org/wiki/Create,_read,_update_and_delete
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CRUD matrix testing

**Goal:** make sure every entity can be created, read, updated and deleted through the intended functions, and only those.

## Build the matrix
Rows = entities (Customer, Order, Invoice). Columns = functions, screens or API endpoints. Cell = letters C/R/U/D the function performs on that entity.

| Entity | Signup | Checkout | Admin panel | Nightly purge |
|---|---|---|---|---|
| Customer | C | R | RUD | D |
| Order | | C | RU | D |
| Invoice | | C | R | |

## Read the matrix for gaps
- **Row without C:** where does this data come from? Migration or import must then be tested.
- **Row without D:** retention or GDPR erasure is missing, or done outside the app.
- **Row without R:** data is written and never shown, so nobody notices it is wrong.
- **Several functions with U:** concurrent-update and last-writer-wins tests.
- **Cell differs per role:** add a role dimension and test denied operations (403, hidden button and direct API call).

## Tests per cell
- C: required fields, defaults, duplicate keys, audit fields set.
- R: every field written is shown correctly in every place it appears (list, detail, export).
- U: partial update leaves other fields untouched; optimistic locking or version conflict.
- D: soft vs hard delete, cascades to children, references from other entities (cannot delete customer with open orders), restore.

## Verify
After a full lifecycle run (create, read in all views, update, delete), a DB query finds no orphan child rows and the audit log has one entry per operation.

## Checked

2026-10-28. Confirmed: Wikipedia CRUD page: create, read, update, delete as the basic operations on persistent data. Removed: Dead ISTQB source link (HTTP 500).

Method: documentation only; no commands were run.
