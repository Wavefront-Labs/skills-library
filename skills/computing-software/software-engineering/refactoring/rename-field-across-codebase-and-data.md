---
id: computing-software.software-engineering.refactoring.rename-field-across-codebase-and-data
name: rename-field-across-codebase-and-data
category: computing-software
field: software-engineering
product: refactoring
tags: [refactoring, organizing-data, rename-field, expand-contract, schema-migration, serialization, fowler-catalog]
level: practitioner
status: draft
description: "Rename a field everywhere it lives - code, database column, JSON payloads, events, caches - using encapsulation and expand-contract so nothing breaks mid-rollout."
sources:
  - https://refactoring.com/catalog/renameField.html
  - https://martinfowler.com/bliki/ParallelChange.html
  - https://www.prisma.io/dataguide/types/relational/expand-and-contract-pattern
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Rename Field (code and persisted data)

In-memory renames are an IDE keystroke (IntelliJ Shift+F6, VS Code F2, Rider Ctrl+R R). The hard part is a field that also lives in a database, a wire format, or other teams' code.

## Code-only mechanics (Fowler)
1. If the record has limited scope, rename all accesses and test - done.
2. Otherwise encapsulate the record first (accessors), so the field name is used in one place.
3. Rename the private field; adjust the accessors; test.
4. If the constructor takes the field name, accept both names temporarily.
5. Rename the accessors (Change Function Declaration), updating callers.

## Persisted or published field: expand-contract (parallel change)
**Database column**
1. Expand: add the new column (nullable). Deploy code that writes both columns and reads the old one.
2. Backfill: `UPDATE ... SET new = old WHERE new IS NULL` in batches (avoid a long lock: 1-10k rows per transaction).
3. Switch reads to the new column; add NOT NULL / constraints when backfill completes.
4. Contract: stop writing the old column; drop it in a later deploy (after rollback window).
Avoid `ALTER TABLE ... RENAME COLUMN` with rolling deploys: old pods still query the old name and fail instantly.

**JSON / API / events**
- Serialisers accept both names on read (`@JsonAlias("old")` in Jackson, Pydantic `validation_alias=AliasChoices("new","old")`, `[JsonPropertyName]` plus a shim in System.Text.Json), write both during migration.
- Mark the old field deprecated in the schema (OpenAPI `deprecated: true`, proto: keep the field number, add `reserved "old_name"` after removal - renaming a proto field keeps the binary wire format but breaks JSON mapping).
- Event streams retain old messages: consumers must read the old name for as long as retention or replay windows exist.

**Caches and search indexes**: entries serialised with the old name; version the cache key or flush.

## Verify
- [ ] Grep (all repos, infra-as-code, dashboards, SQL views, BI queries) for the old name returns nothing before contract.
- [ ] Reconciliation query shows old and new columns equal before switching reads.
