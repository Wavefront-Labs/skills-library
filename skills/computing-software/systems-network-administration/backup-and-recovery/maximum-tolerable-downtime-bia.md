---
id: computing-software.systems-network-administration.backup-and-recovery.maximum-tolerable-downtime-bia
name: maximum-tolerable-downtime-bia
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [business-impact-analysis, bia, mtd, maximum-tolerable-downtime, rto, rpo, nist-sp-800-34, contingency-planning]
level: practitioner
status: docs-checked
description: "Run the BIA step of NIST SP 800-34r1: define MTD, RTO and RPO and how they relate, and record them per mission or business process."
sources:
  - https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-34r1.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Business impact analysis: MTD, RTO and RPO

**Goal:** recovery targets that come from the business's real tolerance for outage, not from what the backup tool happens to do.

## Terms (NIST SP 800-34r1)
- **MTD** (maximum tolerable downtime): the total time the system owner or authorizing official is willing to accept for a mission/business process outage or disruption, including all impact considerations. A poorly determined MTD leaves planners with imprecise direction on the recovery method and the depth of recovery procedures.
- **RTO** (recovery time objective): the maximum time a system resource can remain unavailable before an unacceptable impact on other system resources, the supported processes, and the MTD. It guides selection of technologies. When the RTO cannot be met immediately and the MTD is inflexible, initiate a Plan of Action and Milestones to document and mitigate the gap.
- **RPO** (recovery point objective): the point in time, before the disruption, to which process data can be recovered given the most recent backup copy. Unlike the RTO, RPO is not part of the MTD; it reflects how much data loss the process can tolerate.
- The RTO must ensure the MTD is not exceeded, so it is normally shorter than the MTD; for example, reprocessing time after recovery must be added to the RTO to stay within the MTD.
- The first version of SP 800-34 used the term Maximum Allowable Outage (MAO) for the downtime threshold.

## How the BIA sets them
The contingency plan coordinator analyses the supported processes with process owners, leadership and business managers to determine acceptable downtime if a process or its data were unavailable. Impacts can be expressed in values and units meaningful to the organisation, on a scale that indicates severity if the process could not be performed (for example a "Costs" category in staffing, overtime or fee terms). The MTD, RTO and RPO per process are then recorded, with the drivers for each value (such as a mandate).

## Output table
Columns: mission/business process, MTD, RTO, RPO, and the drivers for each value. Add the system, dependencies and recovery priority from your own analysis.

## Gotchas
- Owners tend to ask for zero for everything until shown the cost; present options with their cost.
- Add detection and decision time to what you compare with the MTD, not just restore time.

## Verify
Every production system has an RTO and RPO agreed by its business owner, and the backup and DR design is checked against them in restore tests.

## Checked

2026-11-09. Read NIST SP 800-34 Rev. 1 section 3.2 (MTD, RTO, RPO definitions and relationship, MAO footnote) and the BIA template tables. Removed: the WRT term and the RTO + WRT formula (not in the document), the 1 hour to 1 week impact grid, the ERP example row, mapping RPO to log shipping or replication, seasonal peaks and dependency-order advice, the 12 hour COOP figure (footnote about MEF systems, not relied on).

Method: documentation only; no commands were run.
