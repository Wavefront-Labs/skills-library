---
id: creative-arts.design-for-form-and-experience.ux-design.running-a-ux-benchmarking-study
name: running-a-ux-benchmarking-study
category: creative-arts
field: design-for-form-and-experience
product: ux-design
tags: [ux-benchmarking, benchmark-study, longitudinal-benchmark, competitive-benchmark, ux-metrics, ux-research]
level: practitioner
status: draft
description: "Run a UX benchmarking study: choose a stable task set and metrics, collect them the same way every cycle, and compare against your baseline or competitors over time."
sources:
  - "Nielsen Norman Group - UX Benchmarking and Quantitative Usability Testing (nngroup.com/articles/ux-benchmarking)"
  - "Tullis and Albert, Measuring the User Experience, 3rd ed. (2022)"
  - "MeasuringU - Benchmarking the user experience (measuringu.com)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# UX benchmarking study

**Goal:** a repeatable measurement of experience quality so changes can be judged against a fixed yardstick.

## Design
1. **Choose scope:** 5-10 top tasks (from analytics or a top-task survey) and the metrics for each: success, time, SEQ, plus a session-level SUS (`creative-arts.design-for-form-and-experience.ux-design.measuring-usability-with-sus-and-seq`).
2. **Choose comparison:** previous release (longitudinal), competitors (competitive), or an industry norm. Competitive studies need the same tasks and the same participant profile on each product, with order counterbalanced.
3. **Sample:** benchmarking needs quantitative power; use 20-30 or more per condition. Unmoderated remote tools (UserZoom, Maze, Lyssna) make this affordable.
4. **Freeze the protocol:** exact task wording, success definitions, participant criteria, device and tool. Write it down; the next cycle must be identical.
5. **Run, analyse, report:** table per task with mean, confidence interval and delta against benchmark. Use a scorecard (red/amber/green against targets set up front).
6. **Cadence:** per major release or quarterly. Re-use the same tasks even when the UI changes; add new tasks rather than replacing.

## Gotchas
- Changing task wording or recruit criteria breaks comparability. Version the protocol.
- Competitor access needs care (logins, region); record which version and date was tested.
- Report intervals, not just means; most apparent differences with small n are noise.

## Verify
- [ ] Protocol document exists and is reused unchanged.
- [ ] Each metric has n, mean, interval and a comparison.
- [ ] Targets were set before the data arrived.
