---
id: business-finance.project-and-program-management.microsoft-project.baselining-and-tracking-progress
name: baselining-and-tracking-progress
category: business-finance
field: project-and-program-management
product: microsoft-project
tags: [project-and-program-management, microsoft-project, ms-project, msp, project-desktop, project-online, baseline, set-baseline, tracking-gantt, status-date, actuals, percent-complete, remaining-duration, update-project, variance, slipping-tasks, re-baseline, schedule-control, scheduling, gantt]
level: practitioner
status: draft
description: "In Microsoft Project: set and maintain baselines, update actuals against a status date, reschedule incomplete work, and read variance tables, Tracking Gantt and slipping-task reports."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Baselining and tracking progress in Microsoft Project

**Goal:** freeze an approved plan as a baseline, record actual progress each period
against a status date, and see variance (slippage and overrun) clearly — so the
schedule is a control tool, not a picture of the original intent.

*Draft: menu paths are for Project desktop (Project Professional / Project Online
desktop client) in recent versions; Microsoft's cloud Project products have changed
names and features over time, so check what your licence includes. Building the
task network itself is covered by
architecture-construction.construction-estimating-scheduling.ms-project.linking-tasks-and-showing-the-critical-path.*

## 1. Before you baseline
- Schedule is complete: all tasks linked (no loose ends except start/finish), no
  unnecessary hard date constraints, durations and resources assigned, and the
  critical path makes sense.
- Plan approved by the sponsor. A baseline of a draft plan is meaningless.

## 2. Set the baseline
*Project tab → Schedule group → Set Baseline → Set Baseline…* → choose **Baseline**
(not Baseline 1–10 for the first one), **Entire project** → OK.
This copies Start, Finish, Duration, Work and Cost into Baseline fields for every task.
- Check it: *View → Tracking Gantt* shows grey baseline bars under the current bars;
  or add the Baseline Start/Baseline Finish columns.
- Approved change later: baseline only the **selected tasks** that changed, tick
  **Roll up baselines to all summary tasks**, and log the change request number in
  a task note. Keep earlier baselines in Baseline 1–10 if you need history.

## 3. Each reporting period: update actuals
1. Set the **status date**: *Project tab → Status Date* (e.g. Friday of the reporting
   week). Everything is reported "as of" this date.
2. Enter progress per task, in the *Tracking* table (*View → Tables → Tracking*):
   **Actual Start**, **% Complete** or **Actual Duration/Actual Work**, **Remaining
   Duration**, **Actual Finish** for done tasks.
   - Update **Remaining Duration** honestly — % complete alone assumes the original
     duration was right.
   - For effort-tracked projects, enter actual work in *Task Usage* (timephased) or
     via timesheets if connected.
3. For tasks exactly on plan, select and use *Task tab → Mark on Track*.
4. Reschedule incomplete work that should have started: *Project tab → Update Project
   → Reschedule uncompleted work to start after* the status date. Otherwise unstarted
   work stays in the past and the forecast is wrong.

## 4. Read the variance
- *View → Tables → Variance* shows Start Var. and Finish Var.; *Tables → Cost* and
  *Work* tables show cost and work variance against baseline.
- Tracking Gantt: red critical tasks, bars right of their grey baselines = slippage.
- Add a **Finish Variance** column on summary tasks and the project summary task
  (*Format → Project Summary Task*) to see the headline slip.
- Built-in reports: *Report tab → In Progress → Slipping Tasks / Late Tasks*;
  *Dashboards → Project Overview / Work Overview*. Filter *Slipping Tasks* in the
  Gantt view for a quick list.

## 5. Report
Status date, forecast finish vs baseline finish, slipping critical tasks with cause
and recovery action, cost/work variance, approved re-baselines.

## Gotchas
- **Re-baselining whole project to hide slippage** — the variance history disappears;
  only re-baseline approved changes, and keep the original in Baseline 1.
- Entering Actual Finish dates in the future (after the status date).
- **Automatic scheduling off** for tasks (manual scheduled mode): they don't move when
  predecessors slip. Check Task Mode is Auto Scheduled.
- Typing over Start/Finish dates creates Start-No-Earlier-Than constraints; use actuals
  fields instead.
- Physical % Complete vs % Complete vs % Work Complete are different fields; pick
  one convention for EV calculations.

## Verify
- [ ] Baseline fields populated for every task (no blank Baseline Finish).
- [ ] Status date set before each update.
- [ ] Incomplete past work rescheduled after the status date.
- [ ] Variance table and Tracking Gantt reviewed; slipping critical tasks listed.
- [ ] Re-baselines limited to approved changes, with prior baseline preserved.
