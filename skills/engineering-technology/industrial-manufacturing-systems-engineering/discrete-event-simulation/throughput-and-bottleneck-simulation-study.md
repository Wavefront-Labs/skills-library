---
id: engineering-technology.industrial-manufacturing-systems-engineering.discrete-event-simulation.throughput-and-bottleneck-simulation-study
name: throughput-and-bottleneck-simulation-study
category: engineering-technology
field: industrial-manufacturing-systems-engineering
product: discrete-event-simulation
tags: [discrete-event-simulation, des, simulation, arena, flexsim, simio, anylogic, plant-simulation, tecnomatix, simpy, throughput, bottleneck, buffer-sizing, warm-up, welch-method, replications, confidence-interval, input-modelling, distribution-fitting, mtbf, mttr, common-random-numbers, scenario-analysis, validation, verification, line-design, queueing]
level: advanced
status: draft
description: "Run a DES study that sizes a line: input distributions, warm-up, replications and confidence intervals, bottleneck detection, buffer-size experiments (Arena/FlexSim/Simio/SimPy)."
sources:
  - "Law, Simulation Modeling and Analysis"
  - "Banks, Carson, Nelson & Nicol, Discrete-Event System Simulation"
  - "Roser et al., active-period bottleneck detection method (published conference papers)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Throughput and bottleneck simulation study

**Goal:** answer a sizing question ("will this line make 420 units/shift, and with
which buffers?") with a validated model and a confidence interval, not a single
animated run.

## 1. Frame the question before opening the tool
Write the decision, the KPI (throughput/h, lead time, WIP, utilisation), the
scenarios to compare and the acceptable precision (e.g. ±2% on throughput at 95%).
Model only what can change the answer: a conveyor's exact geometry rarely matters;
its capacity and transfer time do. The tool (Arena, FlexSim, Simio, AnyLogic,
Plant Simulation, SimPy) matters far less than this step.

## 2. Model the inputs as distributions
- Cycle times: fit from time-study or machine logs; manual work is right-skewed
  (lognormal, gamma, or triangular when data is thin). Never model with means only:
  a line of fixed-time stations hides all the blocking and starving.
- **Breakdowns**: model time-between-failures (often exponential or Weibull) and
  time-to-repair (lognormal/gamma) separately; base TBF on *operating* time, not
  clock time, for wear-driven failures. Availability = MTBF ÷ (MTBF + MTTR).
  Two machines with equal 90% availability behave very differently if one fails
  for 2 min every 18 and the other for 2 h every 18 h; the long repairs need buffers.
- Changeovers, scrap/rework loops, shift patterns and breaks.
Check fits with a Q-Q plot plus a goodness-of-fit test; with large samples the test
rejects everything, so the plot is the better judge.

## 3. Verify and validate
- **Verify** (built right): trace single entities, run deterministic tests, check
  flow balance (in = out + WIP), compare utilisation with hand calculation
  (ρ = arrival rate × service time).
- **Validate** (right model): run the current state and compare with actual
  output and WIP over a real period. Within ~5% on throughput is a common
  acceptance target; agree it with the stakeholder in advance.

## 4. Set run conditions
- **Warm-up**: a line starting empty under-reports WIP and lead time. Use Welch's
  method (moving average of the KPI across replications) and delete data up to where
  it flattens; then set run length to at least ~10× the warm-up.
- **Replications**: for n runs, the 95% CI half-width is h = t(n-1, 0.975) × s ÷ √n.
  Pilot with n0 = 10. Example: mean 431 units/shift, s = 14 → h = 2.262 × 14 ÷ 3.16
  ≈ 10.0. Want ±5 → n ≈ n0 × (h0/h)² = 10 × (10/5)² = **40 replications**.
- **Comparing scenarios**: use common random numbers (same seeds per replication
  across scenarios) and a paired-t CI on the difference. If the CI includes zero, you
  cannot claim one scenario is better.

## 5. Find the bottleneck properly
Highest utilisation is a weak indicator. Use: **blocked/starved** statistics (the
bottleneck is rarely starved or blocked; upstream stations block, downstream starve),
or the **active-period method** (the station with the longest uninterrupted active
periods is the momentary bottleneck; aggregate the shares over time). Confirm with a
sensitivity run: speed the candidate by 10% and see whether throughput moves.

## 6. Run the experiments
For buffer sizing, sweep the buffer in front of and after the bottleneck (e.g. 0,
2, 4, 8, 16) and plot throughput vs total buffer: the curve flattens. Pick the knee,
not the maximum. Use a designed experiment (factorial) when several factors interact,
rather than one factor at a time.

## Gotchas
- One long run is not a substitute for replications unless you use batch means
  correctly.
- Animations convince managers and hide errors; trust the statistics and traces.
- Shift-start effects are real; model breaks and handovers if they are in the data.
- Report the CI, the assumptions and the input data date with every number.

## Verify
- [ ] Decision, KPI and required precision written before modelling.
- [ ] Cycle, failure and repair inputs are fitted distributions, checked with Q-Q plots.
- [ ] Current-state model validated against real output within the agreed tolerance.
- [ ] Warm-up deleted; replication count derived from the target half-width.
- [ ] Scenarios compared with CRN and a paired CI on the difference.
- [ ] Bottleneck confirmed by a sensitivity run, not by utilisation alone.
