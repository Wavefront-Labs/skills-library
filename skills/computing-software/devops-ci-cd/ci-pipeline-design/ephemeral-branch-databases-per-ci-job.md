---
id: computing-software.devops-ci-cd.ci-pipeline-design.ephemeral-branch-databases-per-ci-job
name: ephemeral-branch-databases-per-ci-job
category: computing-software
field: devops-ci-cd
product: ci-pipeline-design
tags: [ci-pipeline-design, branch-databases, neon-branching, test-data-management]
level: advanced
status: docs-checked
description: "Give each CI job or PR its own database: service containers, Testcontainers, template databases, and copy-on-write branching (Neon, PlanetScale) with cleanup."
sources: ["https://neon.com/docs/guides/branching-github-actions", "https://java.testcontainers.org/modules/databases/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ephemeral and branch databases per CI job

Shared test databases cause order-dependent failures. Give each job a private one.

## Options
| Approach | Speed | Realism |
|---|---|---|
| Service container (empty DB + migrations + seed) | fast | schema only |
| Testcontainers in the test process | fast, per suite | schema only |
| Postgres template DB (`CREATE DATABASE t1 TEMPLATE seeded`) | very fast clones | seeded fixture |
| Copy-on-write branch of a staging/anonymised DB (for example Neon) | seconds | production-like data |

## Postgres template trick (parallel workers)
```bash
psql -c "CREATE DATABASE app_template"; migrate up; seed
for i in $(seq 1 $WORKERS); do psql -c "CREATE DATABASE app_test_$i TEMPLATE app_template"; done
```
Template must have no active connections while cloning.

## Neon branch per PR (GitHub Actions)
Neon's branching guide for GitHub Actions uses a `NEON_API_KEY` secret and a `NEON_PROJECT_ID` variable. Follow the guide for the current action names, versions and outputs: create a branch per PR, run migrations and tests against it, and delete it when the PR closes.

## Rules
- Branch from an **anonymised** parent, never raw production with PII.
- Always clean up (scheduled sweeper for orphans older than N days); branches cost storage.
- Run migrations on the branch in CI, which also tests the migration.

## Verify
- [ ] Two concurrent PRs run tests without interfering; branches disappear after merge.

## Checked

2026-10-28. Confirmed: PostgreSQL CREATE DATABASE docs (`TEMPLATE`, and that no other sessions can be connected to the template database while it is copied), Neon GitHub Actions branching guide (`NEON_API_KEY` secret, `NEON_PROJECT_ID` variable), Testcontainers database containers page. Removed: the `neondatabase/create-branch-action@v6` snippet and its inputs and outputs (not shown on the fetched page), and the PlanetScale, Xata and DBLab names.

Method: documentation only; no commands were run.
