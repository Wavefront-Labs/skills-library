---
id: computing-software.software-engineering.csharp-dotnet.testing-ef-core-data-access
name: testing-ef-core-data-access
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, ef-core-testing, testcontainers-dotnet, respawn, in-memory-provider, sqlite-in-memory, ef-core]
level: practitioner
status: docs-checked
description: "Test EF Core code against a real database: why the InMemory provider misleads, SQLite in-memory trade-offs, Testcontainers with migrations, Respawn resets and repository fakes."
sources: ["https://learn.microsoft.com/en-us/ef/core/testing/", "https://learn.microsoft.com/en-us/ef/core/testing/choosing-a-testing-strategy", "https://dotnet.testcontainers.org/", "https://github.com/jbogard/Respawn"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Testing EF Core data access

**Goal:** data-access tests that fail when production would fail - translation errors,
constraints, transactions - and still run fast.

## Strategy (from the EF Core docs)
- Microsoft recommends good test coverage against your real production database system.
  Use a test double only if needed; then prefer the repository pattern over a fake EF Core
  provider or mocking `DbSet`.
- SQLite in-memory is a fallback when the repository pattern is not viable. Providers
  behave differently: SQL Server compares strings case-insensitively by default while
  SQLite is case-sensitive, some queries are unsupported, and provider-specific functions
  fail.
- The EF Core in-memory provider is discouraged and only supported for legacy applications:
  fewer query types, no transactions, no raw SQL.
- A disposable database in a container (Testcontainers, see https://dotnet.testcontainers.org/)
  is one way to get the real database in tests. Share one container per test run through a
  collection fixture rather than starting one per test, and apply real migrations rather than
  `EnsureCreated`.

## Isolation between tests
- **Transaction per test**: begin in the test, never commit, dispose to roll back. Fast; doesn't
  work if code under test commits its own transactions or uses multiple contexts.
- **Respawn**: delete data from all tables (respecting FKs) before each test:
```csharp
_respawner = await Respawner.CreateAsync(conn, new RespawnerOptions { DbAdapter = DbAdapter.Postgres, TablesToIgnore = ["<migrations history table>"] });
await _respawner.ResetAsync(conn);
```
- Unique data per test (random IDs/tenants) allows parallel tests without resets.

## Pitfalls
- Assert with a **new** context instance; the same context returns tracked entities from memory
  and hides mapping bugs.
- Test migrations themselves: migrate an empty DB in CI and a copy of production schema before release.
- Time-dependent queries: inject a clock abstraction so tests control time.

## Verify
- [ ] No `UseInMemoryDatabase` in query/repository tests.
- [ ] Tests run real migrations and pass in CI.

## Checked
2026-11-01. Confirmed against the EF Core "Choosing a testing strategy" page (real database recommended, repository pattern for test doubles, SQLite differences, in-memory provider discouraged with no transactions or raw SQL) and the Respawn README (`Respawner.CreateAsync`, `RespawnerOptions`, `TablesToIgnore`, `DbAdapter`, `ResetAsync`). Removed: the speed/fidelity table, constraint-enforcement claim, the Postgres fixture code and image tag, and the `TimeProvider` name.
Method: documentation only; no commands were run.
