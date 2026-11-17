---
id: computing-software.systems-network-administration.backup-and-recovery.bia-peak-periods-and-time-criticality
name: bia-peak-periods-and-time-criticality
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [time-criticality, peak-periods, business-impact-analysis, bia, mtd, impact-over-time]
level: practitioner
status: docs-checked
description: "Capture peak periods and time criticality in a BIA: how outage impact grows over time, calendar peaks, and setting MTD and RTO for the worst case."
sources:
  - https://csrc.nist.gov/pubs/sp/800/34/r1/upd1/final
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Time criticality and peak periods

**Goal:** RTOs set for the worst moment to lose the system, not an average Tuesday.

NIST SP 800-34 Rev. 1 does not discuss peak periods; the guidance below applies its MTD/RTO definitions with common practice, which is marked as such.

## Impact over time
Ask the owner to rate impact at fixed intervals and chart it. Example only (ratings and intervals are for your organisation to define):

| Outage length | 1 h | 4 h | 1 day | 3 days | 1 week |
|---|---|---|---|---|---|
| Financial | low | low | med | high | severe |
| Regulatory | none | none | low | high | severe |
| Customer | low | med | high | high | severe |

The first column where any category reaches the organisation's "unacceptable" threshold sets the **MTD**. NIST defines the MTD as the total time the system owner or authorizing official will accept for a process outage, including all impact considerations, and says the RTO must normally be shorter than the MTD: if recovering the system leaves reprocessing to do, that time is added to the RTO to stay within the MTD. So RTO = MTD minus catch-up, data re-entry and validation time.

## Peak periods to ask about
Practice, not from the guide:
- Calendar: month-end/quarter-end close, payroll dates, tax deadlines, open enrolment, Black Friday, academic term start.
- Daily: trading hours, batch windows, shift changes, overnight file transfers to partners.
- Event-driven: product launches, regulator submission dates, incident surges (for emergency services).
Record each as a date range with the stricter MTD/RTO that applies.

## Using it
- Where peak RTO is much tighter than normal, consider a seasonal posture: pre-stage the DR environment, freeze changes, raise backup frequency during the window.
- Put the peak calendar in the change-freeze calendar and the DR exercise calendar (do not schedule failover tests inside a peak).
- The guide's cost-balance idea applies: the shorter the RTO, the more the recovery solution costs, so a short peak-only RTO is a cost decision to weigh, not a default.

## Gotchas
- Owners describe the average case unless asked explicitly "when is the worst time for this to fail?".
- Batch jobs with hard external deadlines (bank cut-off times) can make a 2 h outage at 16:00 worse than a 1-day outage on Sunday.

## Verify
Every process in the BIA has an impact-over-time row, a peak-period list (or "none"), and the RTO matches the peak value.

## Checked

2026-11-09. Checked against NIST SP 800-34 Rev. 1 (full PDF from nvlpubs.nist.gov, the document behind the csrc.nist.gov page), section 3.2.1 (MTD, RTO, RPO, cost balancing). Targeted read, not the whole 149 pages. Confirmed: MTD and RTO definitions, RTO shorter than MTD with reprocessing time added to RTO, cost trade-off of shorter RTO. The guide has nothing on peak periods or time buckets, so those parts are labelled example or practice. Removed: the implied authority of the specific table values.

Method: documentation only; no commands were run.
