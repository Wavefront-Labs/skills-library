---
id: engineering-technology.chemical-engineering.process-control.loop-performance-assessment
name: loop-performance-assessment
category: engineering-technology
field: chemical-engineering
product: process-control
tags: [chemical-engineering, process-control, pc-performance-monitoring, loop-performance-assessment, loop-performance, control-performance, loop-assessment]
level: practitioner
status: verified
description: "Assess control loop performance from plant data: time in auto, variability, oscillation, saturation, and benchmarking."
sources:
  - "Harris, T.J. (1989) Assessment of control loop performance, Can. J. Chem. Eng. 67(5):856-861, https://doi.org/10.1002/cjce.5450670519"
  - "Seborg, Edgar, Mellichamp and Doyle, Process Dynamics and Control (textbook, method only)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Loop performance assessment

**Goal:** Assess control loop performance from plant data: time in auto, variability, oscillation, saturation, and benchmarking.

## Steps
1. Compute the basic KPIs: percent of time in automatic, controller output saturation, setpoint changes and the standard deviation of the error.
2. Look at the PV, SP and OP trends for oscillation, sluggishness, noise and valve behaviour.
3. Benchmark using a minimum variance index or an alternative (for example the Harris minimum-variance index, Harris 1989, Canadian Journal of Chemical Engineering 67(5):856-861; it needs the process dead time) when the dead time is known; confirm the method definitions.
4. Prioritise the loops by the economic and safety value and the severity of the poor performance.
5. Retune or fix the instrument and valve problems first before redesign.

## Gotchas
- A poor-looking loop may be limited by the process, not the controller.
- Data compression in the historian distorts the metrics.

## Verify
- [ ] KPIs are computed from uncompressed data.
- [ ] Loops are ranked with the action plan.
