---
id: architecture-construction.construction-estimating-scheduling.delay-analysis.windows-analysis-for-extension-of-time
name: windows-analysis-for-extension-of-time
category: architecture-construction
field: construction-estimating-scheduling
product: delay-analysis
tags: [construction-estimating-scheduling, delay-analysis, forensic-schedule-analysis, windows-analysis, contemporaneous-period-analysis, time-impact-analysis, tia, as-planned-vs-as-built, collapsed-as-built, but-for, extension-of-time, eot, time-extension, concurrency, concurrent-delay, excusable-delay, compensable-delay, critical-path-delay, scl-protocol, aace-29r-03, fragnet, claims, disruption, prolongation]
level: advanced
status: draft
description: "Substantiate an extension of time with a contemporaneous windows/time-impact analysis: pick the method, prepare updates, measure critical-path delay per window and test concurrency."
sources: ["Society of Construction Law Delay and Disruption Protocol, 2nd edition (2017)", "AACE International RP 29R-03 Forensic Schedule Analysis", "AACE International RP 52R-06 Time Impact Analysis"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Windows analysis for an extension of time

**Goal:** show, period by period, which events actually moved the critical path and by
how much, in a way that a contract administrator, adjudicator or expert can follow and
reproduce.

## 1. Choose the method to fit the records and the timing
| Method | When | Needs |
|---|---|---|
| Prospective **time impact analysis (TIA)** | delay happening now, EOT requested under the contract | accepted current update + fragnet |
| **Windows / contemporaneous period analysis** | retrospective; regular updates exist | series of updates with good actuals |
| **As-planned vs as-built** | poor programme, good as-built records | baseline + reliable as-built dates |
| **Collapsed as-built (but-for)** | no usable updates, good as-built | detailed as-built rebuilt with logic |
The SCL Protocol favours dealing with EOT contemporaneously (prospectively) where
possible; check what the contract requires — its notice and programme clauses override
any method preference.

## 2. Prepare the programmes
1. Collect the **baseline/accepted programme** and every update (native files, e.g. P6
   XER, not just PDFs).
2. Validate each update: actuals left of data date, logic intact, no unexplained logic
   or duration changes between updates (diff them; log every change).
3. Gather the **as-built evidence**: daily diaries, RFIs, instructions, minutes,
   photos, delivery tickets. Each event needs a start, an end and a record.
4. Define **windows** — usually each update period, or periods bounded by key events
   or milestones.

## 3. Analyse each window
1. Note the forecast completion date (or key milestone) at the window's start and end.
   The difference is the **critical delay in that window** (positive = slip, negative
   = recovery).
2. Identify the **critical/longest path** at the start and end; trace which activities
   on it slipped and why.
3. Attribute the slip to events using the records: employer risk events (late
   information, variations, access), contractor risk (productivity, resources, sub
   performance) or neutral (exceptionally adverse weather, where the contract allows).
4. For a TIA inside a window: insert a **fragnet** (event activities with durations and
   logic ties) into the update at the event date, reschedule, and measure the change in
   completion. Keep the fragnet minimal and evidenced.
5. Total the windows; the sum should reconcile to the overall slip from baseline to
   actual (or current forecast) completion.

## 4. Concurrency
Concurrent delay = two or more effective causes, one employer-risk and one
contractor-risk, both affecting completion **in the same period**. Test it by checking
whether the contractor event was itself on the critical path at the time, not just
whether it happened. Treatment differs by jurisdiction and contract (e.g. many
common-law approaches give time but not money for true concurrency; apportionment in
some jurisdictions — legal advice needed, not a scheduling call).

## 5. Present it
Per window: one page with dates, the path, the slip, the cause and the evidence
references. Summary table: window, critical slip, employer days, contractor days,
neutral days, concurrent days. Appendix: programme change log and native files.

## Gotchas
- Using an update the other side never accepted, or one with retrospective logic edits.
- Measuring delay to an activity rather than to completion (or the relevant milestone).
- Float ownership: who benefits from float is often set by the contract — read it.
- Mitigation and acceleration: if the contractor recovered time, the window shows a
  smaller slip; don't double-claim.
- Hindsight: a prospective TIA and a retrospective windows analysis can legitimately
  give different answers — say which question you are answering.

## Verify
- [ ] Method chosen and justified against the contract and the records available.
- [ ] Every update validated and the change log between updates is complete.
- [ ] Each window's slip is measured at completion/milestone, on the critical path.
- [ ] Each delay day ties to an event with documentary evidence.
- [ ] Window totals reconcile to overall delay.
- [ ] Concurrency tested on the critical path, and legal treatment left to the contract/lawyers.
