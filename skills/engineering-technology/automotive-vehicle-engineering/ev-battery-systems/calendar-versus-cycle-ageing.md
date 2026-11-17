---
id: engineering-technology.automotive-vehicle-engineering.ev-battery-systems.calendar-versus-cycle-ageing
name: calendar-versus-cycle-ageing
category: engineering-technology
field: automotive-vehicle-engineering
product: ev-battery-systems
tags: [calendar-ageing, cycle-ageing, battery-ageing, sei-growth, arrhenius, capacity-fade, resistance-growth, ageing-model, depth-of-discharge, test-matrix]
level: practitioner
status: gated
description: "Separate calendar from cycle ageing of lithium-ion cells: design the test matrix, fit temperature and SoC dependence, and build a capacity and resistance fade model."
sources:
  - "Plett, Battery Management Systems Vols 1 and 2"
  - "Warner, Lithium-Ion Battery Chemistries and Pack Design (chapter list)"
  - "Linden and Reddy, Handbook of Batteries (chapter list)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Calendar versus cycle ageing

## 1. Definitions
- **Calendar ageing:** loss while resting; depends mainly on temperature and state of charge (SoC) and elapsed time.
- **Cycle ageing:** loss caused by throughput; depends on depth of discharge (DoD), mean SoC, C-rate and temperature.
Both reduce capacity and increase resistance; a cell may lose power before energy, so track both.

## 2. Mechanisms (high level)
SEI growth on the anode consumes lithium and raises resistance (often modelled roughly as square-root of time (gated: unconfirmed, source is paywalled or blocked)); particle cracking, loss of active material and lithium plating (see lithium plating skill) add under cycling. Cathode-specific degradation depends on chemistry; use supplier and literature data for your chemistry.

## 3. Test matrix
Calendar: store cells at several SoC levels (low, mid, high) and temperatures, within the cell's safe storage limits. Cycle: vary DoD and C-rate at fixed temperature; add a few realistic duty-cycle profiles. Use at least three cells per condition and periodic check-ups (reference performance tests: capacity at a low rate, pulse resistance, optionally EIS) with identical conditions each time. Plan months to years; accelerate with temperature only within validated limits.

## 4. Model structure
A common semi-empirical form: Q_loss = Q_cal(T, SoC, t) + Q_cyc(DoD, I, T, Ah_throughput).
The calendar term is often fitted as A(SoC) x exp(-Ea/(R T)) x t^z, with z near 0.5 in many reports (gated: unconfirmed, source is paywalled or blocked); fit it, do not assume it. The cycle term is often a power law of throughput with stress factors. Fit by regression on check-up data; validate on held-out conditions and on real-drive profiles. Model capacity loss and resistance growth separately.

## 5. Use in design
Feed the model with the vehicle usage profile (temperature history, charging habits, SoC window) to predict state of health vs time for warranty and thermal-management requirements (see battery warranty modelling and preconditioning). Keep a conservative bound, not just the mean.

## Verify
- [ ] Calendar and cycle effects separated by experiment design.
- [ ] Check-up protocol identical across time and cells.
- [ ] Model validated on conditions not used for fitting.
- [ ] Uncertainty bounds reported, not just a mean fit.
