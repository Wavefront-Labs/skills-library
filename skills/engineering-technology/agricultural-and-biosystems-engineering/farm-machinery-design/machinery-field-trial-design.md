---
id: engineering-technology.agricultural-and-biosystems-engineering.farm-machinery-design.machinery-field-trial-design
name: machinery-field-trial-design
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: farm-machinery-design
tags: [agricultural-and-biosystems-engineering, farm-machinery-design, machinery-field-trial, experimental-design, randomised-block, machine-comparison, replication, field-trial, machinery-testing]
level: practitioner
status: draft
description: "Design a fair field trial to compare machines or settings: randomised blocks, replication, plot size, measured variables, data checks and statistics."
sources:
  - "Hunt & Wilson, Farm Power and Machinery Management"
  - "ASABE Standards, Engineering Practices and Data (https://www.asabe.org)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Field trial design for machinery comparison

**Goal:** a result that separates the machine or setting effect from field variability.

## Design
1. State the question and the measures: yield, loss, fuel per hectare, time per hectare, quality.
2. Randomised complete blocks: each block holds all treatments in random order; orient blocks along the main field gradient.
3. Replicate at least 3-4 times so you can estimate error; plots long enough for steady state, with end buffers.
4. Control or randomise operator, speed, crop condition and time of day.
5. Record weather, soil moisture and breakdowns.
6. Measure with calibrated scales or checked yield monitors (`yield-monitor-calibration-procedure`).

## Analysis
ANOVA for blocks and treatments, then a mean-separation test (LSD or Tukey) at a stated significance level. Report standard error, not just means. Practical significance matters: a significant 1 percent difference may not justify a change. Unreplicated side-by-side strips are indicative only.

## Verify
- [ ] Layout, randomisation and raw data saved.
- [ ] Residuals checked for outliers and unequal variance.
