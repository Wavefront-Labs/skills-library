---
id: computing-software.data-engineering.data-quality.lineage-and-root-cause-triage
name: lineage-and-root-cause-triage
category: computing-software
field: data-engineering
product: data-quality
tags: [data-quality, data-lineage, column-level-lineage, openlineage, dbt-lineage, root-cause-analysis, incident-triage, impact-analysis, datahub, marquez, postmortem, dag-diff]
level: practitioner
status: draft
description: "Trace a bad number back to its source quickly using column-level lineage, and run a disciplined root-cause triage instead of guessing."   # quoted: YAML would cut an unquoted value at " #" or choke on ": "
sources:
  - https://openlineage.io/docs/
  - https://docs.getdbt.com/reference/node-selection/graph-operators
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Root-cause triage for a bad number — stop guessing, trace the graph

**Goal:** when a stakeholder says "this number looks wrong," find the actual root cause (which upstream change, which run, which row) in minutes, not a day of Slack archaeology.

## 1. Table-level vs column-level lineage — know which you have
- **Table-level lineage** (dbt's own DAG, most warehouse "lineage" views) tells you table A feeds table B — useful for "what depends on this table if I change it" impact analysis, useless for "which specific *column* caused this specific wrong number" when a table has 40 columns and only one is implicated.
- **Column-level lineage** (OpenLineage with column-level facets, dbt's `exposure`/catalog combined with SQL parsing, some commercial catalogs like DataHub/Atlan) traces a specific output column back through every transformation to its specific source columns — this is what you actually need for triage, and most teams only have table-level, which is why triage is slow. If column-level lineage isn't available, approximate it by reading the relevant model's SQL directly for the column in question rather than guessing from the table-level graph.

## 2. The triage order — cheapest checks first
1. **Is this a real data change or a calculation change?** Diff the metric's SQL definition against the last known-good version (`git log`/`git diff` on the dbt model, or the BI tool's saved query) before assuming the data is wrong — a silently-changed `WHERE` clause or JOIN condition is a very common "bad number" cause that has nothing to do with data quality.
2. **Did the run actually succeed and complete?** Check the orchestrator (Airflow/Dagster) run log for the relevant DAG for partial failures, skipped tasks, or a run that's still the previous day's stale data because today's hasn't landed yet. This single check resolves a large fraction of "wrong number" reports.
3. **Walk the lineage graph one hop at a time from the reported table**, checking each upstream table's row count and a key aggregate (sum/count) against its own expected range, rather than jumping straight to the raw source — the break is usually at a specific transformation step, and checking every hop in order finds it faster than guessing where it "probably" is.
4. **Check the actual source system** only after confirming the pipeline faithfully reproduced what it ingested — re-pulling from source to "double check" before ruling out a transformation bug wastes the most time in most triages.

## 3. Impact analysis — the other direction
Before changing a column's logic or removing it, use lineage **downstream**: dbt's `dbt ls -s +my_model+` (or the graph API) to list every model depending on it, cross-referenced with BI tool lineage (which dashboards/reports query those models) if available. Changing a widely-depended-on column without this check is how "a small cleanup" becomes a multi-team incident — the review step is cheap; the incident isn't.

## 4. Closing the loop — make the next incident faster
Every root-cause triage that takes more than it should reveals a lineage/observability gap — log it as a specific, fixable gap (e.g. "column-level lineage missing for this transformation," "no test existed on the column that actually broke") rather than closing the incident once the immediate number is fixed. A triage process that doesn't feed back into test/lineage coverage repeats the same slow investigation every time a similar break happens.

## Verify
- [ ] The triage checked for a logic/definition change before assuming a data problem (step 1), with a timestamp showing which check ran first.
- [ ] Lineage was walked hop-by-hop from the reported symptom, not jumped straight to the raw source.
- [ ] A downstream impact-analysis check (who depends on this) exists and was run before any production column change, not just before major schema changes.
- [ ] The root cause, once found, resulted in a new test or lineage annotation at the specific break point — not just a one-off data fix.
