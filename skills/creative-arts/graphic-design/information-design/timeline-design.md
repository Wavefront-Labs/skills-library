---
id: creative-arts.graphic-design.information-design.timeline-design
name: timeline-design
category: creative-arts
field: graphic-design
product: information-design
tags: [graphic-design, information-design, timeline-design, timeline, chronology, time-scale, gantt, event-timeline]
level: practitioner
status: draft
description: "Design timelines that read correctly: proportional or ordinal scale, one time axis, label hierarchy, spacing for dense periods, and honest handling of gaps."
sources:
  - https://helpx.adobe.com/illustrator/user-guide.html
  - https://helpx.adobe.com/indesign/user-guide.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Timeline design

**Goal:** a timeline where the order and spacing of events are accurate and the labels remain readable.

## 1. Decide the scale
- **Proportional (true scale):** distance on the axis equals time. Use it when intervals matter (project schedules, history spans). Dense periods will crowd, so plan callouts.
- **Ordinal (sequence only):** equal spacing regardless of date. Use it when the order matters more than duration, and **say so** (a note such as "not to scale").
- Broken or segmented axes (a zig-zag for a long gap) must be marked clearly.

## 2. Orientation and axis
- Horizontal reads well for short sequences and wide formats; vertical suits scrolling pages and long lists.
- Draw one axis, with ticks at regular intervals (years, quarters, days). Label ticks sparsely.

## 3. Events
- Distinguish **points** (milestones: a marker) from **spans** (bars from start to end date).
- Label hierarchy: date, short title, optional one-line description. Alternate labels above and below the axis, or use leader lines, to avoid collisions.
- Group related events by lane (swimlanes) for different actors or categories; use consistent colours with a legend.
- Highlight the few events that matter; do not give 30 items equal weight.

## 4. Build notes
- Illustrator: place events from a data table using precise positions (Align and Transform panels); for Gantt-style charts use a spreadsheet or charting tool, then clean up in the design app.
- Keep dates in one format (ISO 8601 style, 2026-10-18, is unambiguous in data; use the audience's format on the final graphic).
- Mark the present with a "today" line on forward-looking timelines.

## Failure modes
- Mixed scales on one axis.
- Overlapping labels at dense periods.
- Uncertain dates presented as exact; show approximate dates with a "c." or a range bar.

## Self-check
Measure two intervals on the graphic: the ratio matches the dates (if proportional). Check every label is attached unambiguously to its marker.
