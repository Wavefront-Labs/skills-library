---
id: computing-software.devops-ci-cd.deployment-strategies.databases-during-blue-green
name: databases-during-blue-green
category: computing-software
field: devops-ci-cd
product: deployment-strategies
tags: [deployment-strategies, blue-green-database, blue-green, expand-contract]
level: advanced
status: docs-checked
description: "Handle the database in blue-green deployments: one shared schema with expand/contract, read-only cutover windows, and why two databases rarely work."
sources: ["https://martinfowler.com/bliki/BlueGreenDeployment.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Databases during blue-green

Blue and green app fleets are cheap to duplicate; the database is not. Both fleets almost always
share one database, so at cutover both versions must work against the same schema.

## Shared database with expand/contract
1. **Expand** (before deploying green): add new columns/tables, nullable or with defaults; no drops,
   no renames. Blue keeps working.
2. Deploy green; it writes both old and new shapes if needed (dual-write) and reads the new.
3. Switch traffic. Blue idle but **still compatible**, so switching back is safe.
4. Backfill, then later release **contract**: drop old columns once blue is gone and no rollback is planned.

## Options when the schema cannot be compatible
- Short **read-only window**: put the app in read-only mode, migrate, switch, re-enable writes.
- Two databases with replication (logical replication blue->green, cut over, reverse replication
  for rollback). Complex; reserve for cases where one shared schema cannot work.

## Pitfalls
- Rolling back to blue after green wrote data in a new format: blue must tolerate it (ignore unknown
  values, nullable columns).
- Long-running migrations during cutover hold locks; run expand ahead of the release.
- Caches and queues are shared too: message schema changes need the same compatibility rule.

## Verify
- [ ] Blue test suite passes against the expanded schema; switching back after green writes data loses nothing.

## Checked

2026-10-28. Confirmed from Martin Fowler's BlueGreenDeployment article: keep the blue environment as a backup while green is live, and the option of putting the application in read-only mode before cut-over. Removed: the Postgres 15 to 17 and AWS RDS Blue/Green example (not in the sources) and the blocked O'Reilly book link. Expand/contract is presented as a general technique, not a sourced claim.

Method: documentation only; no commands were run.
