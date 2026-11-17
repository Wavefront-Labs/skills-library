---
id: computing-software.database-administration.sql-server.azure-sql-serverless-and-auto-pause
name: azure-sql-serverless-and-auto-pause
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, azure-sql-database, serverless-azure-sql, auto-pause, vcore-dtu]
level: practitioner
status: docs-checked
description: "Decide when Azure SQL Database serverless fits, set min/max vCores and auto-pause delay, and handle resume delay and billing behaviour."
sources:
  - https://learn.microsoft.com/en-us/azure/azure-sql/database/serverless-tier-overview
  - https://learn.microsoft.com/en-us/cli/azure/sql/db#az-sql-db-update
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Azure SQL serverless and auto-pause

## Model
Serverless is a compute tier for single databases that scales compute automatically within a range you set and bills
compute per second. When the database is paused, compute cost is zero and only storage is billed. Storage is billed
as in the provisioned tier. It is available in the General Purpose and Hyperscale service tiers, vCore purchasing
model (not DTU), on Standard-series (Gen5) hardware; Business Critical is not supported.

## Billing
- Usage between your minimum and maximum: compute cost is based on vCores and memory used.
- Usage below the minimum: cost is based on the configured minimum vCores and minimum memory.
- Paused: no compute cost. See the "Serverless compute tier billing" page for calculations and minimum bill; this
  skill does not quote prices.

## Fits / does not fit
Well suited: single databases with intermittent, unpredictable usage and lower average utilisation, databases that are
frequently rescaled, and new databases whose size is hard to estimate.
Use provisioned instead for: regular, predictable, higher average utilisation; databases that cannot tolerate memory
trimming or delay when resuming from pause; many intermittent databases that can be consolidated into an elastic pool.

## Configure
```bash
az sql db update -g <RESOURCE_GROUP> -s <SERVER_NAME> -n <DB_NAME> \
  --edition GeneralPurpose --compute-model Serverless --family Gen5 \
  --min-capacity 0.5 --capacity 4 --auto-pause-delay 60
```
- `--min-capacity` and `--capacity` set the minimum and maximum vCores; memory and IO limits are proportional to the
  vCore range. Default minimum is 0.5 vCores (allowed values depend on the maximum; see resource limits).
- Auto-pause delay: General Purpose minimum 15 minutes, Hyperscale minimum 60 minutes; maximum 10,080 minutes (seven
  days) in 1-minute steps; default 60; `-1` disables auto-pause.

## Auto-pause and resume
- The database resumes on the next login or other activity. The first connection after a pause sees lower
  responsiveness, and connectivity errors during resume are predictable, so every client needs connection retry logic.
- Auto-pause and auto-resume are available in General Purpose; for Hyperscale they are a preview feature.
- Some features and settings prevent auto-pause; if you rely on them, disable auto-pause. See the "Troubleshooting
  auto-pause" and "Troubleshooting auto-resume connectivity" pages for the list and error details.
- Serverless can trim memory more often than provisioned compute, which affects performance-sensitive workloads.

## Verify
After the configured delay with no activity the database shows as paused (see "Monitor the serverless compute tier"
for pause and resume events), and a client with retry logic connects successfully after resume.

## Checked
Date: 2026-11-09. Confirmed against "Serverless compute tier for Azure SQL Database" (Microsoft Learn): model, billing
rules, tiers and hardware, scenarios, defaults and ranges, retry and auto-pause guidance; the `az sql db update` flags
were matched to the CLI reference by the review tooling. Removed (not on the page): the 50-60% break-even figure,
3 GB-per-vCore memory ratio, error 40613 text, the list of what blocks pausing, `sys.dm_db_resource_stats` query and
Azure Monitor metric names.
Method: documentation only; no commands were run.
