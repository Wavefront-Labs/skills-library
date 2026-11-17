---
id: computing-software.devops-ci-cd.deployment-strategies.declarative-schema-migrations-atlas-sqitch
name: declarative-schema-migrations-atlas-sqitch
category: computing-software
field: devops-ci-cd
product: deployment-strategies
tags: [deployment-strategies, atlas-schema, sqitch, database-migrations]
level: advanced
status: draft
description: "Manage database schema with declarative (Atlas) or dependency-based (Sqitch) migration tools in CI/CD: plan, diff, lint, approval and apply against each environment."
sources: ["https://atlasgo.io/declarative/apply", "https://sqitch.org/docs/manual/sqitchtutorial/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Declarative schema tools (Atlas and Sqitch)

## Atlas (declarative or versioned)
Desired state in HCL/SQL; Atlas computes the diff.
```bash
# plan against a live DB (dev URL is a throwaway DB used for normalisation)
atlas schema apply --url "$DATABASE_URL" --to file://schema.sql \
  --dev-url "docker://postgres/16/dev" --dry-run
# versioned flow: generate a migration file from the desired state
atlas migrate diff add_orders --dir file://migrations --to file://schema.sql --dev-url docker://postgres/16/dev
atlas migrate lint --dir file://migrations --dev-url docker://postgres/16/dev --latest 1
atlas migrate apply --dir file://migrations --url "$DATABASE_URL"
```
`atlas.sum` protects migration directory integrity; CI fails if files were edited after generation.
Lint detects destructive changes (drop column/table), backward-incompatible renames and table locks.

## Sqitch (change-based, dependency graph)
```bash
sqitch add orders --requires customers -n "Add orders table"   # deploy/revert/verify scripts
sqitch deploy db:pg://app@db/app
sqitch verify db:pg://app@db/app
sqitch revert --to @HEAD^ db:pg://app@db/app
```
`sqitch.plan` orders changes by dependencies, not timestamps; each change has a verify script.

## Pipeline shape (either tool)
1. PR: generate/lint migrations, apply to an ephemeral DB, run tests.
2. Show the plan (Atlas `--dry-run` output) in the PR or deploy approval.
3. Apply before the app rollout (expand phase); contract later.

## Verify
- [ ] CI fails on a migration that drops a column without an approval; apply on staging matches the plan.
