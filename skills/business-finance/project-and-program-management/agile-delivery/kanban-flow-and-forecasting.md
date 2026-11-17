---
id: business-finance.project-and-program-management.agile-delivery.kanban-flow-and-forecasting
name: kanban-flow-and-forecasting
category: business-finance
field: project-and-program-management
product: agile-delivery
tags: [project-and-program-management, agile-delivery, agile, kanban, wip-limits, work-in-progress, cycle-time, lead-time, throughput, littles-law, cumulative-flow-diagram, cfd, work-item-age, service-level-expectation, monte-carlo, forecasting, flow-metrics, scrum, stand-up, classes-of-service, no-estimates]
level: practitioner
status: draft
description: "Run Kanban flow: visualise the workflow, set and lower WIP limits, track cycle time, throughput, ageing and CFDs, and forecast with percentiles and Monte Carlo."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Kanban flow: WIP limits, cycle time and probabilistic forecasting

**Goal:** get work through a team faster and more predictably by limiting work in
progress, measuring flow, and forecasting delivery from real data instead of estimates.

## 1. Visualise the real workflow
- Board columns = the actual stages work passes through (e.g. *Ready → Analysis →
  Build → Review → Test → Done*), split into **doing / done** sub-columns where hand-offs
  wait. Map it as it is, not as the process document says.
- One card per item of roughly similar size; mark types (feature, defect, support)
  with classes of service (standard, fixed-date, expedite).
- Write **explicit policies** on the board: definition of ready/done per column,
  who pulls, expedite rules (e.g. max one expedite item at a time).

## 2. Limit WIP
- Set a **WIP limit** per column (or per team). Starting point: roughly the number of
  people working that stage, or total team WIP ≈ team size, then lower it gradually.
- When a column is full, people **stop starting and start finishing**: help
  downstream, swarm on blocked items, pair on review.
- **Little's Law:** average cycle time = average WIP ÷ average throughput. With
  throughput constant, halving WIP halves cycle time. (Holds for averages in a
  stable system.)

## 3. Measure flow (weekly)
- **Cycle time** — start to done for each item. Plot on a **scatterplot**; read the
  85th percentile ("85% of items finish within 9 days"). Averages hide the tail.
- **Throughput** — items finished per week.
- **WIP** and **work item age** — how long in-progress items have been open. Ageing
  items beyond the 85th-percentile cycle time are the ones to swarm on today.
- **Cumulative flow diagram (CFD):** widening bands show WIP growing in a stage —
  a bottleneck forming.
- Flow efficiency (active ÷ total time) if you track blocked/waiting time.

## 4. Forecast with data
- **Single item:** "We'll finish this within 9 days with 85% confidence" (from the
  cycle-time percentile). Service-level expectation (SLE) is this number.
- **Many items ("when will these 40 be done?"):** run a **Monte Carlo simulation**
  sampling historical weekly throughput thousands of times; report dates at 50/85/95%
  confidence. Spreadsheets or free tools can do it.
- Needs ~10+ weeks of throughput history and roughly consistent item sizing (split
  big items). No story-point estimation required.

## 5. Cadences
Daily stand-up walking the board **right to left** (closest to done first, focus on
blocked and ageing items); replenishment meeting to pull new work; weekly/biweekly
flow review of metrics and policies; delivery planning; retros.

## Scrum teams too
These metrics work inside Scrum: WIP limits within a sprint, throughput-based sprint
forecasting, ageing work in the daily scrum.

## Gotchas
- WIP limits set high "just to start", never lowered — no effect.
- Ignoring blocked items: they still count against WIP, which is the point; it forces
  someone to unblock them.
- **Expedite abuse:** if half the work is expedite, nothing is.
- Measuring individuals' throughput → gaming; measure the system.
- Changing the "start" point of cycle time between periods breaks comparisons.

## Verify
- [ ] Board reflects the real workflow with explicit column policies.
- [ ] WIP limits exist, are respected, and have been revised from data.
- [ ] 85th-percentile cycle time and weekly throughput are tracked.
- [ ] Ageing items beyond the SLE are discussed at stand-up.
- [ ] Multi-item forecasts are Monte Carlo ranges with confidence levels, not single dates.
