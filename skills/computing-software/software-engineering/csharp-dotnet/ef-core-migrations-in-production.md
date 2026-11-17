---
id: computing-software.software-engineering.csharp-dotnet.ef-core-migrations-in-production
name: ef-core-migrations-in-production
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, dotnet, ef-core, ef-migrations, idempotent-scripts, migration-bundles, schema-changes, zero-downtime, dotnet-ef, ef-data-seeding]
level: practitioner
status: docs-checked
description: "Create, review and deploy EF Core migrations safely: idempotent SQL scripts or bundles instead of Migrate() at startup, data-loss checks and zero-downtime changes."
sources:
  - https://learn.microsoft.com/en-us/ef/core/managing-schemas/migrations/
  - https://learn.microsoft.com/en-us/ef/core/managing-schemas/migrations/applying
  - https://learn.microsoft.com/en-us/ef/core/managing-schemas/migrations/managing
  - https://learn.microsoft.com/en-us/ef/core/cli/dotnet
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# EF Core migrations in production

**Goal:** schema changes that are reviewed like code, applied once by the pipeline,
and never drop data by surprise.

## Create and review
```bash
dotnet tool install --global dotnet-ef
dotnet ef migrations add AddOrderStatus -p src/Infra -s src/Api
dotnet ef migrations script <PreviousMigration> AddOrderStatus -o review.sql
```
Read the generated migration AND the SQL. A migration may drop a column when the intent was to rename it; fix that by hand with `migrationBuilder.RenameColumn`.

## Applying: pick one, not Migrate() on startup
| Method | Use |
|---|---|
| `dotnet ef migrations script --idempotent -o migrate.sql` | DBA-reviewed SQL run by the pipeline; safe to rerun |
| `dotnet ef migrations bundle --output artifacts/efbundle` | executable built in CI and run later without the SDK, tools or source: `./efbundle --connection "$CS"` (add `--self-contained` to include the .NET runtime) |
| `context.Database.Migrate()` at app start | only for local dev / single-instance apps |
EF Core 9 and later use migration locking, but startup migration still means the app needs DDL permissions and a failed migration fails app startup.

## Zero-downtime changes (expand / contract)
Old and new app versions run side by side during deploy, so each migration must be
compatible with the PREVIOUS code:
1. Add nullable column / new table (expand). Deploy code writing both.
2. Backfill in batches (raw SQL or a job), not in a single giant UPDATE.
3. Switch reads; then make NOT NULL / drop old column in a later release (contract).
Renames = add new + copy + drop old across releases.

## Other practices
- Custom SQL in migrations: `migrationBuilder.Sql("...")` for data fixes and views. EF wraps each migration in a transaction where it can; some operations cannot run in a transaction on some databases, so check the provider notes.
- Do not use the current `DbContext` or entity CLR types to move data in a migration; historical migrations must keep compiling.
- Never edit a migration already applied anywhere; add a new one.
- Keep the migration files and the model snapshot (`*ModelSnapshot.cs`) under source control; `dotnet ef migrations remove` removes the last unapplied migration.

## Verify
- [ ] CI applies all migrations to an empty DB and to a copy of the prod schema.
- [ ] `dotnet ef migrations has-pending-model-changes` (added in EF Core 8.0) fails CI if a migration is missing.
- [ ] Generated SQL reviewed for drops, locks and long-running statements.

## Checked

Checked 2026-10-25 against dotnet/EntityFramework.Docs (managing-schemas/migrations: index, applying, managing; cli/dotnet) on main.
Confirmed: migration strategies (SQL script, bundle, tools, runtime) and that EF Core 9+ uses migration locking; `dotnet ef migrations script --idempotent`; `dotnet ef migrations bundle --output`, `--self-contained` and `efbundle --connection`; `has-pending-model-changes` added in EF Core 8.0; `RenameColumn`; `migrationBuilder.Sql`; per-migration transactions; model snapshot; `migrations remove`.
Removed as unconfirmed: the exact scaffold warning text, the `-r linux-x64` option, the PostgreSQL `CONCURRENTLY` note, squashing and snapshot-conflict advice, crash-loop wording.

Method: documentation only; no commands were run.
