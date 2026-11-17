---
id: computing-software.devops-ci-cd.deployment-strategies.flyway-and-liquibase-in-the-pipeline
name: flyway-and-liquibase-in-the-pipeline
category: computing-software
field: devops-ci-cd
product: deployment-strategies
tags: [deployment-strategies, database-change-management, flyway, liquibase, schema-migration, database-migrations, migrate-job, flyway-validate, liquibase-update-sql, changelog-lock, kubernetes-job, helm-hook, migrations-in-ci]
level: practitioner
status: draft
description: "Run Flyway or Liquibase migrations as a pipeline stage: validate and dry-run SQL on PRs, migrate as a separate job before rollout, lock handling, and Kubernetes Job/Helm hook patterns."
sources: ["https://documentation.red-gate.com/fd/command-line-184127404.html", "https://docs.liquibase.com/commands/home.html", "https://dora.dev/capabilities/database-change-management/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Flyway and Liquibase in the pipeline

## Shape of the pipeline
```
PR:     lint migrations -> migrate a throwaway DB (testcontainers/service) -> tests
        -> print the SQL that would run against prod (dry run) for review
Deploy: backup/snapshot check -> migrate job (once) -> app rollout -> smoke test
```
Migrations run as **one dedicated step**, not at app startup in every replica (racing
replicas, long locks during rollout, no clear failure point).

## Flyway
Files: `db/migration/V20261016_1200__add_orders_status.sql` (versioned, immutable once
applied), `R__views.sql` (repeatable, re-applied when checksum changes).
```bash
flyway -url="$JDBC_URL" -user="$DB_USER" -password="$DB_PASS" \
  -locations=filesystem:db/migration info
flyway ... validate          # fails if an applied migration's checksum changed or is missing
flyway ... migrate
```
- Settings via `flyway.toml` / env `FLYWAY_URL` etc.; never put passwords on the command
  line in logs.
- `outOfOrder=false` (default) in prod; timestamped versions avoid collisions between
  branches.
- Dry run SQL (`-dryRunOutput`) is a Teams/Enterprise feature; on Community, review
  migration files themselves.
- Never edit an applied migration; `flyway repair` only to fix checksums after an
  approved, deliberate change.

## Liquibase
`changelog.yaml` including changeSets with `id` + `author`; tracked in
`DATABASECHANGELOG`, concurrency guarded by `DATABASECHANGELOGLOCK`.
```bash
liquibase --changelog-file=db/changelog.yaml --url="$JDBC_URL" status --verbose
liquibase ... update-sql > pending.sql        # dry run: exact SQL for review/approval
liquibase ... update
liquibase ... tag "release-$VERSION"           # rollback target
```
- `validate` checks changelog syntax and checksums.
- Stuck lock after a killed job: `liquibase release-locks` (only after confirming no
  other migration is running).

## Kubernetes patterns
- A `Job` per release (`migrate-<version>`), the pipeline waits:
  `kubectl wait --for=condition=complete job/migrate-1.42 --timeout=15m`, then deploys.
- Helm: `helm.sh/hook: pre-upgrade,pre-install` with `hook-delete-policy:
  before-hook-creation,hook-succeeded`; failed hook fails the release before pods change.
- Argo CD: `argocd.argoproj.io/hook: PreSync` or sync-wave -1.
- Migration image = the app image (same commit) with a different command; keeps code and
  schema versions aligned.

## Safety rules
- Backward-compatible (expand/contract) migrations only, so the old app version keeps
  working during rollout and after an app rollback.
- Separate DB user for migrations (DDL rights) from the app user (DML only).
- Set `lock_timeout`/`statement_timeout` (Postgres) in the migration session so a blocked
  `ALTER TABLE` fails fast instead of queuing all traffic behind it.

## Verify
PR job shows `Successfully applied N migrations` on a fresh DB and `validate` passes
against a prod-like snapshot; deploy log shows the migrate job completed before the
rollout started.
