---
id: computing-software.firmware-embedded-development.hardware-debugging.jitter-measurement
name: jitter-measurement
category: computing-software
field: firmware-embedded-development
product: hardware-debugging
tags: [timing-analysis, jitter-measurement, period-jitter, release-jitter, histogram, scope-persistence, logic-analyzer-timing, control-loop-timing, firmware-embedded-development]
level: advanced
status: draft
description: "Measure timing jitter of periodic firmware activities (control loops, sampling, PWM updates): scope persistence and histograms, logic-analyser exports, and finding the sources."
sources:
  - https://www.tek.com/en/documents/primer/understanding-and-characterizing-timing-jitter
  - https://support.saleae.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Jitter measurement for firmware

**Goal:** quantify how much a periodic event deviates from its ideal timing, and trace the
deviation to its cause.

## Definitions that matter for firmware
- **Period jitter**: variation of the interval between consecutive events (e.g. control loop
  runs at 1 ms +/- x).
- **Release/start jitter**: delay from the ideal trigger (timer interrupt) to when the work
  actually starts.
- **Completion jitter**: variation in when outputs are written (affects actuator timing).
Report min/max (peak-to-peak) and standard deviation; control and audio care about peak values.

## Measuring
1. Toggle a GPIO at the event of interest (start of the loop body, output write).
2. **Scope**: trigger on the previous edge, view the next with infinite persistence: the smear
   width is peak-to-peak period jitter. Use the scope's period/width statistics and histogram
   functions over thousands of cycles.
3. **Logic analyser**: capture minutes, export edge timestamps to CSV, compute intervals in a
   script:
   ```python
   import numpy as np
   t = np.loadtxt("edges.csv", delimiter=",", skiprows=1, usecols=0)
   d = np.diff(t[::2])            # rising-to-rising
   print(d.mean(), d.std(), d.min(), d.max())
   ```
4. In-firmware: store DWT timestamps of each event in a ring buffer and compute statistics
   (cheaper, but includes measurement overhead jitter).

## Common sources and fixes
| Source | Fix |
|---|---|
| Work started from a task, preempted/delayed by others | raise priority, or do the timing-critical part in the timer ISR / DMA |
| Interrupt masking (critical sections, long ISRs) | shorten critical sections; use priority split (zero-latency ISR) |
| Flash wait states / cache misses vary | run hot code from RAM/TCM |
| Tick-based scheduling (1 ms tick resolution) | hardware timer for the period |
| Clock source jitter (RC oscillator) | crystal/PLL |
| Variable-length code paths before the output write | write outputs first thing in the cycle (from previous computation) |
Hardware-triggered outputs (timer compare, DMA from timer) have near-zero jitter: prefer them
for the actual output edge.

## Verify
- [ ] Jitter statistics recorded under worst-case system load (all tasks, comms, logging on).
- [ ] Value compared against the requirement (e.g. control loop jitter < 1 % of period).
