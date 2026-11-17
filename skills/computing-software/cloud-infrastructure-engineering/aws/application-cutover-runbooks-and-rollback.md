---
id: computing-software.cloud-infrastructure-engineering.aws.application-cutover-runbooks-and-rollback
name: application-cutover-runbooks-and-rollback
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, migration, application-cutover, cutover-runbook, rollback-plan, go-no-go, hypercare]
level: practitioner
status: docs-checked
description: "Run migration cutovers that can be rolled back: T-minus plan, go/no-go criteria, final sync checks, DNS switch, validation, point of no return, reverse replication and hypercare."
sources: ["https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Monitoring.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Application cutover runbooks and rollback

## T-minus plan
| When | Action |
|---|---|
| T-14 days | lower DNS TTLs to 60 s on names that will move; confirm change approval and comms |
| T-7 | full rehearsal in a test environment with timings; freeze non-essential changes |
| T-2 | confirm replication healthy (MGN replication healthy, DMS CDC latency near zero), test instances validated |
| T-1 | go/no-go meeting; on-call roster for cutover and hypercare |
| T-0 | execute runbook |

## Runbook steps (each with owner, command, expected result, duration)
1. Announce start; put source app in maintenance/read-only mode (stop writes).
2. Wait for final sync: DMS `CDCLatencySource`/`CDCLatencyTarget` ~0 and validation clean; MGN final sync / launch cutover instances.
3. Stop replication tasks once in sync (record the source log position for reverse replication).
4. Start target applications; run smoke tests (login, key transactions, integrations, batch jobs).
5. Data validation: row counts, checksums on key tables, business reconciliation queries.
6. Switch traffic: DNS records / load balancer targets / connection strings.
7. Monitor errors, latency, business KPIs for the agreed observation window.
8. **Point of no return** decision: after this, rollback means data reconciliation, not a switch back.
9. Announce completion; finalise MGN cutover (see the MGN guide for what it archives and removes).

## Go/no-go criteria
Written beforehand: replication lag threshold, smoke tests all green, no Sev1/2 incidents open,
key people present, rollback rehearsed. Any "no" means reschedule, not improvise.

## Rollback
- Before point of no return: switch DNS back, re-enable writes on source; nothing written to target is lost if the target took no writes.
- After writes on target: **reverse replication** (DMS task target -> source started at cutover) keeps the source current so rollback stays possible for days.
- Keep source systems intact (powered off, not deleted) through hypercare.

## Hypercare
1-4 weeks of heightened monitoring, daily check-ins, fast-track fixes; then decommission sources
following data retention requirements.

## Verify
- [ ] Rehearsal timings fit the window with 30% buffer.
- [ ] Rollback steps tested in rehearsal, including reverse replication.

## Checked

2026-10-28

Confirmed: CDCLatencySource and CDCLatencyTarget task metrics and their use to find the cause of latency (DMS User Guide, monitoring page).

Removed: MGN Healthy state name, MGN finalise side effects; replaced prose sources with the DMS page (the MGN and Prescriptive Guidance pages were not fetched, so the T-minus timings are process advice, not documented figures).

Method: documentation only; no commands were run.
