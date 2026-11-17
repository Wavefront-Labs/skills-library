---
id: creative-arts.design-for-form-and-experience.interaction-design.laying-out-a-dashboard
name: laying-out-a-dashboard
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [dashboard-layout, dashboard-design, kpi-cards, information-hierarchy, data-dashboard, data-display, chart-selection]
level: practitioner
status: draft
description: "Lay out a dashboard and choose charts for it: start from decisions, put KPIs top-left, group by task, pick chart types by question, keep ink low and states designed."
sources:
  - "Stephen Few, Information Dashboard Design, 2nd ed. (Analytics Press, 2013)"
  - "Edward Tufte, The Visual Display of Quantitative Information (1983)"
  - "Nielsen Norman Group - Dashboards: Making Charts and Graphs Easier to Understand (nngroup.com/articles/dashboards-preattentive)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dashboard layout and chart selection

**Goal:** the right information at a glance for a defined audience and decision.

## Start with decisions
Who uses it, how often, and what decisions or actions follow? Write the 5-8 questions the dashboard must answer; drop everything else.

## Layout
1. **Hierarchy:** the most important KPIs top-left (F-scan) as **big numbers with context** (change vs previous period, target, sparkline).
2. **Group** related metrics in cards or regions with headings; summary first, then detail; a consistent grid (`creative-arts.design-for-form-and-experience.interaction-design.building-column-grids-and-gutters`).
3. One screen for glance; drill-down for detail (click a chart to open a filtered table).
4. **Global controls** (date range, segment) in one place at top, applied to all widgets with the state visible.
5. Limit to roughly 5-9 widgets above the fold; avoid scrolling for the main story.

## Choosing charts (by question)
- **Compare categories:** horizontal bars (sorted) or columns.
- **Trend over time:** line (area only for volume); sparklines in KPI tiles.
- **Part-to-whole:** stacked bar or a single bar; pie only with 2-4 slices.
- **Distribution:** histogram, box plot.
- **Relationship:** scatter. **Ranking:** sorted bars. **Single value vs target:** bullet graph (not gauges).
- Avoid 3D, dual axes, dense legends; direct labels; start bars at zero; consistent colour per category and CVD-safe palette.

## States
Loading skeletons, empty, error and stale-data indicators ("Updated 10:04"); tables with text alternative for charts; keyboard-reachable tooltips.

## Verify
- [ ] Each widget answers a listed question; KPIs show context.
- [ ] Chart type matches the question; axes honest.
- [ ] Global filters clear; states and accessibility covered.
