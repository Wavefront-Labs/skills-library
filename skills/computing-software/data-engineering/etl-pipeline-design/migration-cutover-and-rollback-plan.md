---
id: computing-software.data-engineering.etl-pipeline-design.migration-cutover-and-rollback-plan
name: migration-cutover-and-rollback-plan
category: computing-software
field: data-engineering
product: etl-pipeline-design
tags: [etl-pipeline-design, data-migration, cutover-plan, rollback-plan, go-no-go, freeze-window, consumer-repointing, warehouse-migration]
level: advanced
status: draft
description: "Plan the cutover of a data platform migration: readiness criteria, freeze and final sync, consumer repointing order, go/no-go checkpoints, rollback triggers and decommissioning."
sources:
  - https://cloud.google.com/architecture/migration-to-gcp-getting-started
  - https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-database-migration/cutover.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Migration cutover and rollback plan

**Goal:** switching consumers from the old warehouse/pipeline to the new one is a rehearsed, reversible event, not a hopeful weekend.

## Readiness criteria (before scheduling cutover)
- Parallel run for N cycles (e.g. 2-4 weeks incl. a month-end) with reconciliation passing: row counts, checksums, key metric totals within tolerance.
- All consumers inventoried (BI dashboards, extracts, reverse ETL, APIs, ad hoc users) with owners and a tested connection to the new platform.
- Performance: critical dashboards/queries meet SLAs on the new platform.
- Access: roles, row/column policies, service accounts replicated and tested.
- Runbook written and **rehearsed** at least once in a staging/dry-run cutover.

## Cutover runbook skeleton
| T | Step | Owner | Check |
|---|---|---|---|
| T-7d | announce freeze window, confirm go/no-go meeting | lead | |
| T-1d | freeze: no schema/pipeline changes on old platform | all | change log empty |
| T-0 00:00 | stop old ingestion writers (or keep dual-running) | platform | |
| T-0 00:15 | final incremental sync old -> new | data eng | watermark equal both sides |
| T-0 01:00 | reconciliation suite | data eng | all pass |
| T-0 01:30 | **go/no-go #1** | lead | |
| T-0 02:00 | repoint consumers in order: internal batch jobs -> BI semantic layer/connections -> extracts/reverse ETL -> external APIs | owners | smoke test each |
| T-0 06:00 | **go/no-go #2** (business validation of key reports) | business | sign-off |
| T+1..14d | hypercare: old platform read-only and kept in sync (or snapshot) | all | |
| T+30d | decommission old platform | platform | backups archived |

Use DNS/connection aliases, semantic-layer data sources or a config switch so repointing is a config change, not editing hundreds of dashboards.

## Rollback
Define **triggers** up front (e.g. reconciliation failure on tier-1 metric, critical dashboard broken > 2 h, data loss) and **mechanism**:
- Old platform kept warm (pipelines running or able to restart from the frozen point) during hypercare.
- Repointing reversible (aliases switch back).
- Writes that happened only on the new platform after cutover must be replayable back or accepted as lost; minimise by keeping source-of-truth ingestion dual-running.
Decide who can call rollback and the deadline after which rollback is no longer possible.

## Communication
Status channel, timeline with checkpoints, consumer-facing FAQ (new connection strings, known differences e.g. SQL dialect, timezone behaviour).

## Gotchas
- Month-end/quarter-end differences show up only on those dates: include them in the parallel run.
- Scheduled exports with hard-coded hosts are the usual stragglers; search code repos and scheduler configs for old hostnames.
- Decommissioning too early removes the rollback path and audit history.

## Verify
- [ ] Rehearsal completed with timings; runbook updated from lessons.
- [ ] Post-cutover: zero queries hitting the old platform from production service accounts (query logs).
