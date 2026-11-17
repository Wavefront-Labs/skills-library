---
id: architecture-construction.construction-estimating-scheduling.ms-project.linking-tasks-and-showing-the-critical-path
name: linking-tasks-and-showing-the-critical-path
category: architecture-construction
field: construction-estimating-scheduling
product: ms-project
tags: [construction-estimating-scheduling, ms-project, microsoft-project, msp, project-online, gantt-chart, construction-programme, programme, task-linking, dependencies, predecessors, finish-to-start, start-to-start, lag, lead, critical-path, total-slack, free-slack, float, auto-scheduled, manually-scheduled, constraints, baseline, tracking-gantt, cpm]
level: intro
status: draft
description: "Build a logic-driven construction programme in Microsoft Project: link tasks with FS/SS/FF and lags, avoid constraints, show the critical path and slack, and baseline it."
sources: ["Microsoft Support documentation for Project desktop (critical path, task links, baselines)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Linking tasks and showing the critical path in MS Project

**Goal:** turn a list of construction activities into a programme whose dates are driven
by logic, not typed in, so that the critical path Project shows is real and the
programme reacts correctly when something slips.

## 1. Set the file up first
1. **Project › Project Information:** set the Start Date; schedule *from Project Start
   Date* (scheduling from finish date makes every task As Late As Possible).
2. **Project › Change Working Time:** build the site calendar — 5- or 6-day week, site
   hours, public holidays, any industry shutdown (e.g. the Christmas break). Assign it
   as the project calendar.
3. **File › Options › Schedule:** set *New tasks created:* **Auto Scheduled**. Manually
   scheduled tasks (pin icon) ignore logic and are the most common cause of a "dead"
   programme.
4. Set default duration units to days and check *Hours per day* matches the calendar
   (e.g. 8). A mismatch makes "1 day" mean the wrong number of hours.

## 2. Structure, then durations
- Use summary tasks (indent with `Alt+Shift+Right`) for the WBS: Preliminaries, Substructure,
  Frame, Envelope, Fit-out, Services, Commissioning, Handover. **Never link summary
  tasks** — link the work tasks beneath them.
- Durations in working days, from quantities ÷ crew output where you can (see the
  quantity-takeoff and cpm-scheduling skills in this field).
- Add milestones (duration 0) for possession, watertight, power-on, practical completion.

## 3. Link the logic
Type into the **Predecessors** column using task IDs:
| Entry | Meaning | Typical use |
|---|---|---|
| `12` | Finish-to-Start | pour slab after rebar finishes |
| `12SS+3d` | Start-to-Start, 3-day lag | blockwork follows frame by 3 days |
| `12FF+2d` | Finish-to-Finish, 2-day lag | services finish 2 days after ceilings |
| `12FS+7ed` | FS with 7 *elapsed* days | concrete cure regardless of calendar |
Rules of thumb:
- Every task needs at least one predecessor and one successor (except the start and
  finish milestones). Open ends hide float.
- Prefer real intermediate tasks over long lags; a 20-day lag is a missing activity.
- Avoid negative lags (leads) except where a genuine overlap exists.
- **Don't type dates** into Start/Finish — doing so creates *Start No Earlier Than*
  constraints. Check the Indicators column for the calendar-icon constraint marker.

## 4. Show the critical path and slack
1. In Gantt Chart view: **Format › Bar Styles group › tick Critical Tasks** (and
   Slack) — critical bars turn red.
2. Insert columns **Total Slack** and **Free Slack**.
3. Filter: **View › Filter › Critical**. For a reliable chain, also check
   **File › Options › Advanced › Tasks are critical if slack is less than or equal to
   0 days**, and tick *Calculate multiple critical paths* only if you want each
   end-chain shown (unverified wording — varies by version).
4. Use **Task Path** (Format › Task Path › Driving Predecessors) on the finish
   milestone to trace what actually drives it.

## 5. Baseline and track
**Project › Set Baseline › Baseline (Entire project)** once the programme is agreed.
Use **Tracking Gantt** to see current vs baseline bars; update with Actual Start,
Actual Finish and Remaining Duration, and set the **Status Date** (Project › Status
Date) before updating so incomplete work is moved past it.

## Gotchas
- A task with a *Must Start On* or *Finish No Later Than* constraint can show negative
  slack or hide the true path. Use deadlines instead of constraints for target dates.
- Resource levelling (Resource › Level) can move tasks silently — check *Leveling
  Delay* column.
- Inserting a task between linked tasks with *Autolink* may relink things you didn't
  intend; check the predecessors after inserts.
- "Critical" on a summary bar just means a child is critical.
- Effort-driven scheduling changes durations when you add resources to fixed-units tasks.

## Verify
- [ ] No manually scheduled tasks remain (filter or look for the pin icon).
- [ ] Every work task has a predecessor and successor; no links on summaries.
- [ ] Constraint indicators reviewed; only deliberate ones remain.
- [ ] Critical path runs continuously from start to completion milestone.
- [ ] Changing a critical task's duration moves completion; changing a high-slack one doesn't.
- [ ] Baseline set and visible in Tracking Gantt.
