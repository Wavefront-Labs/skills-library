---
id: computing-software.data-engineering.data-modelling.declarative-schema-management-with-atlas
name: declarative-schema-management-with-atlas
category: computing-software
field: data-engineering
product: data-modelling
tags: [data-modelling, atlas-schema, declarative-schema, schema-migrations, schema-as-code]
level: advanced
status: docs-checked
description: "Manage database schemas declaratively with Atlas: desired-state HCL/SQL, diffing and planning migrations, linting destructive changes, and CI/CD workflows."
sources:
  - https://atlasgo.io/getting-started
  - https://atlasgo.io/declarative/apply
  - https://atlasgo.io/lint/analyzers
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Declarative schema management (Atlas)

**Goal:** define the schema you want; let the tool compute and review the migration, with safety checks for destructive changes.

## Declarative apply
The desired state can be an HCL or SQL schema definition, a database URL, or an external schema such as an ORM. By default `atlas schema apply` manages only schemas, tables and their indexes and constraints (views, functions, triggers, roles, permissions and similar are Atlas Pro).

Steps Atlas takes: load the desired state into the dev database (`--dev-url`), inspect the target's current state, plan the migration, then prompt for approval and apply.
```bash
atlas schema apply -u "$DATABASE_URL" --to file://schema.sql --dev-url "docker://postgres/17/dev?search_path=public" --dry-run
atlas schema apply -u "$DATABASE_URL" --to file://schema.sql --dev-url "docker://postgres/17/dev?search_path=public"
```
- Required flags: `--url/-u`, `--to`, `--dev-url`. `--dry-run` prints the planned SQL without executing; `--auto-approve` skips the prompt (not recommended in production); `--edit` opens the plan in an editor; `--schema` and `--exclude` narrow scope; `--env` and `--config` use atlas.hcl.
- The dev database is a throwaway one Atlas loads the desired state into (for example a `docker://` URL).
- `atlas schema inspect --url "$DATABASE_URL" --format '{{ sql . }}'` prints the current schema as SQL.

## Approval and review policy
- Default is manual review: Atlas prints the SQL and asks.
- Atlas Pro can auto-approve based on a review policy in atlas.hcl: `lint { review = ERROR }` (manual review only if the lint report has errors), `WARNING` (warnings or errors), or `ALWAYS` (default). A review policy replaces `--auto-approve`; with it set the flag fails.
- Without a terminal (CI), Atlas applies what the policy approves and a change needing review fails at the prompt. The documented workflow is to pre-plan with `atlas schema plan` and use the policy as fallback for safe unplanned transitions.

## Versioned workflow (reviewable files)
```bash
atlas migrate diff initial --to file://schema.sql --dev-url "docker://postgres/17/dev?search_path=public"
atlas migrate lint --dev-url "docker://postgres/17/dev?search_path=public" --latest 1
atlas migrate apply --url "$DATABASE_URL"
```
`migrate diff` writes a timestamped SQL file into `migrations/` plus an `atlas.sum` checksum file; commit both. The commands assume the default `file://migrations` directory (use `--dir` otherwise).

## Lint analyzers
Examples from the analyzers page:
- destructive: drops of schemas, tables, non-virtual columns (DS101-DS103); lint exits with code 1 when found, configurable in atlas.hcl.
- data-dependent: for example adding a unique index to an existing column (MF101), a non-nullable column (MF103) or making a nullable column non-nullable (MF104); reported by default but does not fail lint unless configured.
- incompatible: renaming or dropping tables and columns (BC101-BC104).
- constraint drops (CD101-CD103).
- blocking (Atlas Pro): table-locking or rewriting changes (PostgreSQL PG3xx, MySQL MY110-MY148); an `-- atlas:nolint` directive can silence a diagnostic.

## Practice
- Declarative for dev speed; versioned files plus lint for production pipelines.
- Keep one tool in charge of a schema.

## Verify
After deployment, `atlas schema apply ... --dry-run` against the target reports no changes.

## Checked
Method: docs-only read on 2026-11-09 of declarative/apply (first 100 lines plus flag searches), lint/analyzers (search of check codes and analyzer sections) and getting-started (inspect, migrate diff and lint sections); all three pages are large, so this was a partial read. Removed or corrected: the HCL schema example (not confirmed on the pages), the claim that lint analyzers flag "NOT NULL without default" specifically, "backward-incompatible renames" wording, the `atlas schema diff` verification command, and the guidance on data-migration backfills and ORM tooling.
