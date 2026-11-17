---
id: computing-software.systems-network-administration.backup-and-recovery.cost-of-downtime-modelling
name: cost-of-downtime-modelling
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [cost-of-downtime, business-impact-analysis, bia, mtd, rto, outage-impact]
level: practitioner
status: docs-checked
description: "Estimate cost of downtime per system for a BIA: revenue, productivity, recovery and penalty components, impact curves over time, RTO spend."
sources:
  - https://csrc.nist.gov/pubs/sp/800/34/r1/upd1/final
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cost of downtime modelling

NIST SP 800-34 Rev. 1 (section 3.2.1) has the BIA characterise outage impacts and estimated downtime, and says impact values can be expressed in units meaningful to the organisation, using a scale (its example is a "Costs" category in staffing, overtime or fee-related terms). It also describes cost balancing: the longer a disruption continues the more costly it is, while the shorter the RTO the more expensive the recovery solution, and the intersection of the two cost lines is an optimal point that differs per organisation. A cost model turns "critical" into numbers for that decision.

## Components (per hour of outage, per system or business process; practice)
| Component | How to estimate |
|---|---|
| Lost revenue | revenue through the process per hour x % that is lost (not deferred) |
| Lost productivity | affected staff x loaded hourly cost x % unable to work |
| Recovery cost | overtime, contractors, expedited hardware, vendor support |
| Contractual penalties | SLA credits, late fees, per-hour clauses |
| Regulatory | fines, mandatory notifications, audit costs |
| Data re-entry | records lost since last recovery point x time to recreate (links to RPO) |
| Reputational/customer churn | estimate conservatively or score qualitatively |

## Impact is not linear
Build a curve by interval of your choosing. Many processes have a cliff (payroll on payday, month-end close, shipping cut-off) where impact jumps. The point where impact becomes unacceptable informs the **MTD**; the guide says the RTO must normally be shorter than the MTD because reprocessing time is added to recovery time.

## Worked example (hypothetical figures)
Order processing: 40,000 revenue per hour with 30% truly lost = 12,000 per hour; 60 idle staff at 50 per hour = 3,000 per hour; so 15,000 per hour in running cost. SLA penalties start at hour 4 as a flat 20,000. Cumulative: 1 h = 15,000; 4 h = 60,000 + 20,000 penalty; 24 h = 360,000 + 20,000 penalty, plus churn. Compare that curve with the annual cost of a faster recovery option: if cutting the RTO from 24 h to 2 h avoids hundreds of thousands per incident, a modest standby is easy to justify, while a much more expensive option may not be. Use your own figures; these are illustrations.

## Process
1. Interview process owners (finance validates numbers).
2. Record assumptions next to each figure; ranges are fine (low/likely/high).
3. Map processes to IT systems and dependencies.
4. Feed the curve into RTO/RPO decisions and recovery tier assignment.
5. Review when the business changes materially; NIST says to update the BIA after significant change.

## Gotchas
- IT estimating business numbers alone produces fiction: get owner sign-off.
- Deferred revenue (customers come back later) isn't lost; ask about substitutability.
- Seasonality changes the curve; document peak-period values separately.

## Verify
Each Tier 1 system has a signed-off impact curve, MTD, and RTO/RPO derived from it, and
recovery spend decisions reference those numbers.

## Checked

2026-11-09. Checked against NIST SP 800-34 Rev. 1 (PDF behind the csrc.nist.gov page), sections 3.2.1 (impact scales, MTD/RTO, cost balancing, Figure 3-3) and 3.6 (BIA update on significant change). Targeted reads, not the whole 149 pages. Confirmed: user-defined impact units, cost-balance logic, RTO shorter than MTD. The component table and worked example are practice and hypothetical; currency symbols and the invented standby prices were removed and the arithmetic re-checked (12,000 + 3,000 = 15,000 per hour). Removed: the "annually" review and fixed interval buckets.

Method: documentation only; no commands were run.
