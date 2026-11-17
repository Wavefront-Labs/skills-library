---
id: architecture-construction.construction-estimating-scheduling.primavera-p6.updating-a-p6-schedule-and-reading-float
name: updating-a-p6-schedule-and-reading-float
category: architecture-construction
field: construction-estimating-scheduling
product: primavera-p6
tags: [construction-estimating-scheduling, primavera-p6, p6, oracle-primavera, schedule-update, progress-update, data-date, actual-start, actual-finish, remaining-duration, retained-logic, progress-override, total-float, free-float, critical-path, longest-path, baseline, variance, f9-schedule, scheduling-log, out-of-sequence, programme-update, cpm, xer]
level: practitioner
status: draft
description: "Run a monthly Primavera P6 update: set data date, enter actuals and remaining durations, reschedule (F9), and read total float and critical path without fooling yourself."
sources: ["Oracle Primavera P6 Professional user documentation", "AACE International RP 29R-03 Forensic Schedule Analysis (update practice context)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Updating a P6 schedule and reading float

**Goal:** produce a clean period update in Primavera P6 — true actuals, honest remaining
durations, a fresh data date — and read the resulting float and critical path correctly
so the update tells the team (and later a delay analyst) what really happened.

## 1. Before you touch anything
1. **Copy the project** (right-click › Copy, or File › Export to XER) and name it with the
   update number and data date, e.g. `UPD07_DD-2026-10-31`. Never progress the only copy:
   each update must survive as its own record.
2. Confirm a **baseline** is assigned (Project › Assign Baselines). Without one, variance
   columns read zero and nobody notices slippage.
3. Check **Tools › Schedule › Options** (F9 › Options) and write the settings down; they
   change results:
   - *Schedule progressed activities using:* **Retained Logic** (the usual contract
     expectation) vs **Progress Override** vs Actual Dates. Retained Logic keeps the
     remaining work of an out-of-sequence activity waiting on its predecessor.
   - *Calculate float based on finish date of:* each project / open projects.
   - *Compute Total Float as:* **Finish Float** (late finish − early finish) is common;
     "smallest of start/finish" gives more pessimistic values.
   - *Define critical activities as:* total float ≤ 0 **or** longest path. Pick one and
     state it in the narrative.

## 2. Collect progress, don't invent it
Gather from site diaries / foremen for every activity in progress or due to start:
actual start, actual finish, and **remaining duration in working days** (not % complete
guessed in the office). Rule of thumb: if remaining duration is unknown, ask "how many
more working days, at the current crew?" — that is the number P6 needs.

## 3. Enter the update
1. Filter to activities with early start before the new data date + one period
   (a "look-ahead" filter) so you don't miss anything.
2. For each: tick **Started** and enter Actual Start; tick **Finished** with Actual Finish
   when complete; otherwise set **Remaining Duration**. Duration % complete type should
   normally be *Duration* or *Physical*; be consistent across the project.
3. No actual date may be **after** the new data date, and no unfinished work may sit
   **before** it.
4. Set the new data date in the Schedule dialog (F9 › Current data date) and **Schedule**.
   Optionally use Tools › Update Progress for a bulk "as planned" progress — only for
   genuinely on-plan level-of-effort items; it hides reality otherwise.

## 4. Read the scheduling log (every time)
F9 › **Log to file** / View Log. Look for: activities without predecessors or successors
(open ends), **out-of-sequence progress**, constraints that were not met, and activities
with actuals after the data date. Fix logic, re-schedule, re-read until the log is clean
or every remaining item is explained.

## 5. Reading float and the critical path
- Add columns: Total Float, Free Float, BL Project Finish, Variance – BL Project Finish
  Date, Longest Path flag (column names vary slightly by version — unverified).
- Group by Total Float, sort ascending. Negative float = the plan no longer meets a
  constraint or the contract completion; the most negative chain is the driving path.
- **Longest path** (Layout › Filter › Longest Path) is more reliable than "TF ≤ 0" when
  there are multiple calendars or constraints — float differences across calendars make
  TF misleading.
- Compare update-to-update: an activity whose float dropped by 15 days this period
  matters more than one with a static −3.

## Gotchas
- **Hard constraints** (Mandatory Start/Finish) break logic and manufacture false
  float; prefer Start On or After / Finish On or Before, or none.
- **Resource leveling** silently shifts dates; don't level during an update unless the
  contract programme was leveled.
- Large float on a key activity usually means a missing successor, not a lucky trade.
- Mixed calendars (5-day vs 7-day, concrete cure on 7-day) make float values not
  comparable across activities.
- Editing original durations or logic in an update without logging it destroys the
  audit trail — keep a revision log of every logic change.

## Verify
- [ ] Update saved as a separate project/XER named with its data date.
- [ ] Every activity left of the data date is actualised; none right of it has actuals.
- [ ] Schedule options (retained logic, float definition, critical definition) recorded.
- [ ] Scheduling log reviewed; open ends and out-of-sequence items fixed or explained.
- [ ] Critical/longest path identified and compared with last update; float erosion noted.
- [ ] Forecast completion vs baseline and contract dates stated in the narrative.
