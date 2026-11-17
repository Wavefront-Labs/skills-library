---
id: computing-software.systems-network-administration.patch-management.war-room-remediation-tracker
name: war-room-remediation-tracker
category: computing-software
field: systems-network-administration
product: patch-management
tags: [remediation-tracker, war-room, emergency-patching, tracking, patch-management]
level: practitioner
status: draft
description: "Run a war-room remediation tracker during an emergency patch: one source of truth per asset, columns, status flow, owner assignment, burn-down and reporting cadence."
sources:
  - https://csrc.nist.gov/pubs/sp/800/61/r3/final
  - https://csrc.nist.gov/pubs/sp/800/40/r4/final
  - https://sre.google/sre-book/managing-incidents/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# War-room remediation tracking

During an emergency, everyone asks "how many left?". One tracker answers it; side spreadsheets create conflicting numbers.

## Tool
Shared sheet or ticket board (Jira/ServiceNow) with one row per affected asset. Seed it from the exposure assessment (scanner hits + inventory query) and keep adding as discovery finds more.

## Columns
| Column | Notes |
|---|---|
| Asset / IP / environment | unique key |
| Exposure | internet-facing, internal, isolated |
| Owner (team + named person) | |
| Version found | |
| Action | patch / mitigate / isolate / decommission |
| Status | New -> Assigned -> In progress -> Done (pending verify) -> Verified / Exception |
| Compromise check | not started / clean / indicators |
| Evidence | scan ID, command output link |
| ETA / blockers | |
| Updated at / by | |

## Rules
- Only "Verified" (rescan or version check) counts as closed.
- Every row has an owner within 1 hour of being added.
- Status meeting every N hours walks only blocked and overdue rows.
- New discoveries are added immediately with a source column.

## Reporting
- Burn-down by exposure class: internet-facing first.
- Headline numbers for comms: total, verified, in progress, blocked, exceptions.
- Export snapshot at each status update for the PIR timeline.

## Gotchas
- Duplicate rows for the same host via IP and hostname; normalise on asset ID.
- Rows marked Done by owners without verification; security verifies.
- Tracker abandoned once the urgent part is over; keep it until the last exception has an owner and date.

## Verify
Tracker totals match scanner rescan results; closure report generated from the tracker and attached to the PIR.
