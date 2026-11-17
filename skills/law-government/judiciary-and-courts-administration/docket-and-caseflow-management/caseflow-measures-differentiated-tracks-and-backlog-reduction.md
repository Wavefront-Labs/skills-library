---
id: law-government.judiciary-and-courts-administration.docket-and-caseflow-management.caseflow-measures-differentiated-tracks-and-backlog-reduction
name: caseflow-measures-differentiated-tracks-and-backlog-reduction
category: law-government
field: judiciary-and-courts-administration
product: docket-and-caseflow-management
tags: [judiciary-and-courts-administration, docket-and-caseflow-management, caseflow-management, case-management, calendaring, listing, docket-control, clearance-rate, time-to-disposition, age-of-pending-caseload, trial-date-certainty, courtools, ncsc, time-standards, differentiated-case-management, dcm, case-tracks, backlog-reduction, continuance-policy, adjournments, early-case-management, triage, inventory-audit, settlement-conferences, master-calendar, individual-calendar]
level: advanced
status: draft
description: "Manage a court's caseload: measure clearance, age and trial-date certainty, assign differentiated case tracks, control continuances, and run a backlog-reduction plan."
sources: [National Center for State Courts CourTools performance measures, Model Time Standards for State Trial Courts (NCSC 2011)]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Caseflow measures, differentiated tracks and backlog reduction

**Goal:** cases resolved within published time standards, with hearings that happen on
the date set. The core idea of caseflow management: **the court, not the parties,
controls the pace of litigation.** Measures here follow the US National Center for State
Courts' CourTools and model time standards; other systems (e.g. listing offices in
Commonwealth courts, the CEPEJ framework in Europe) use similar metrics under different
names.

## 1. Measure first
Core indicators, computed per case type and monthly:
| Measure | Formula / meaning | Reading |
|---|---|---|
| **Clearance rate** | Outgoing cases ÷ incoming cases × 100 | <100% means backlog is growing |
| **Time to disposition** | % of cases resolved within time standards (e.g. 75/90/98% percentiles) | Compare to standards |
| **Age of active pending caseload** | Age distribution of open cases | Shows the backlog's tail |
| **Trial date certainty** | % of trials held on the first (or second) date set | Low certainty = wasted preparation, more continuances |
| Backlog | Pending cases older than the time standard | The target for reduction |
Before trusting numbers, run an **inventory audit**: physically or electronically confirm
that "pending" cases are truly active. Many backlogs contain closed-but-not-recorded or
dormant cases. Case-status codes must be consistent across the court.

## 2. Time standards
Adopt published standards per case type (e.g. a share of general civil cases resolved
within 12 months, misdemeanours within months, felonies within a year — confirm the
standards the court or state has adopted). Make them public, measured and reported.

## 3. Differentiated case management (DCM)
Not all cases need the same process. At filing or the first case-management event,
**triage** into tracks:
- **Expedited**: simple, few parties, little discovery — short fixed timetable.
- **Standard**: ordinary schedule with set milestones.
- **Complex**: many parties, expert-heavy — individual judge, tailored scheduling orders,
  early and frequent conferences.
Criteria should be objective (claim type, value, number of parties, expert need) with
judicial override. Each track has its own milestones and time standard.

## 4. Early and continuous court control
- **Early case management conference**: set realistic, firm dates for every event through
  trial.
- **Meaningful events**: each hearing should accomplish something; avoid "status checks"
  that only adjourn.
- **Continuance (adjournment) policy**: written policy, requests in writing, good cause
  required, decided by a judge, reasons recorded; track continuance rates by cause. Firm
  trial dates drive settlement.
- Calendar design: individual calendars (one judge owns a case) improve accountability;
  master calendars spread work — hybrid systems are common. Set realistic **overbooking**
  levels for trial calendars based on historic fall-out rates.
- Integrate ADR (settlement conferences, mediation) at points where it works best.

## 5. Backlog reduction plan
1. Audit and clean the inventory.
2. Sort backlog by age and type; identify causes (judicial vacancy, missing documents,
   interpreter shortages, lab delays, failure to appear).
3. Targeted actions: dedicated backlog dockets or temporary judges; dismissal for want of
   prosecution after notice for dormant civil cases (per rules); bulk scheduling of
   readiness reviews; fixing upstream bottlenecks with partner agencies.
4. Prevent new backlog: hold clearance rate ≥100% on incoming cases while working the old ones.
5. Report progress publicly monthly.

## Gotchas
- Measuring averages instead of distributions hides very old cases.
- Clearing old cases by closing them administratively without due process.
- Overbooked calendars that make trial dates uncertain, which in turn causes more
  continuances.

## Verify
- [ ] Inventory audited; pending case counts match reality.
- [ ] Clearance rate, time to disposition, age of pending and trial-date certainty reported monthly by case type.
- [ ] Every case assigned to a track with milestones at the first event.
- [ ] Written continuance policy with recorded reasons and tracked rates.
- [ ] Backlog plan has named causes, actions, owners and monthly targets.
