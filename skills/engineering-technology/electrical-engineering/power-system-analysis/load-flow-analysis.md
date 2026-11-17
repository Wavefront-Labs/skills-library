---
id: engineering-technology.electrical-engineering.power-system-analysis.load-flow-analysis
name: load-flow-analysis
category: engineering-technology
field: electrical-engineering
product: power-system-analysis
tags: [load-flow, power-flow, newton-raphson, gauss-seidel, fast-decoupled, per-unit, slack-bus, pv-bus, pq-bus, voltage-regulation, reactive-power, transformer-taps, contingency-analysis, n-1, ansi-c84-1, en-50160, matpower, pandapower, etap, psse, powerfactory, losses, power-system-analysis, bus-type-classification, load-flow-convergence-troubleshooting]
level: practitioner
status: gated
description: "Set up, solve and interpret a load-flow study: per-unit data, bus types, Newton-Raphson, voltage limits per ANSI C84.1/EN 50160, loading and N-1."
sources:
  - "Grainger & Stevenson, Power System Analysis"
  - "Glover, Overbye & Sarma, Power System Analysis and Design"
  - "ANSI C84.1, Electric Power Systems and Equipment - Voltage Ratings (60 Hz)"
  - "EN 50160, Voltage characteristics of electricity supplied by public distribution networks"
  - "IEEE Std 3002.2, Recommended Practice for Conducting Load-Flow Studies of Industrial and Commercial Power Systems"
  - "MATPOWER user's manual"
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# Load-flow analysis — from one-line to defensible voltage and loading results

**Goal:** solve steady-state bus voltages, branch flows and losses for every credible
operating case, and decide whether voltages, thermal loading and reactive margins are
acceptable — not just get a converged answer.

## 1. Build the model in per unit
- Choose a system MVA base (e.g. 100 MVA for transmission, 10 MVA for an industrial
  plant) and the nominal kV of each zone as voltage base.
- Convert nameplate impedances: `Z_new = Z_old · (kV_old/kV_new)² · (MVA_new/MVA_old)`.
- Lines/cables: R, X, B per km × length. Transformers: %Z on own base, X/R, tap
  position and tap range; model off-nominal taps explicitly, not by tweaking kV.
- Loads: constant-PQ for normal studies; use constant-current or -impedance for
  low-voltage scenarios and motor starting, where PQ loads exaggerate collapse.

## 2. Assign bus types
- **Slack (swing)**: one per island — the utility point or largest generator; fixes V and angle.
- **PV**: generators/STATCOMs regulating voltage, with Qmin/Qmax.
- **PQ**: everything else.
Enable Q-limit enforcement: a PV bus at its limit becomes PQ and voltage drops —
exactly the condition you want to see.

## 3. Solve
Newton–Raphson is the default (quadratic convergence, typically 3–6 iterations; the pandapower snippet below was run on case14 and converges, min voltage 1.01 pu);
fast-decoupled is fine for high X/R transmission; Gauss–Seidel only for tiny teaching
cases. Mismatch tolerance around 0.1 kW/kvar on an industrial model, or 1e-8 pu in
research tools. Quick open-source check:
```matlab
% MATPOWER
mpc = loadcase('case14');
opt = mpoption('pf.alg','NR','pf.enforce_q_lims',1);
r = runpf(mpc, opt);
```
```python
import pandapower as pp, pandapower.networks as pn
net = pn.case14(); pp.runpp(net, algorithm="nr", enforce_q_lims=True)
print(net.res_bus.vm_pu.min(), net.res_line.loading_percent.max())
```
Non-convergence usually means data error (wrong base, ohms entered as pu, a tap at
the wrong side) or a genuinely infeasible case — check the largest mismatch bus first.

## 4. Interpret against criteria
- **Voltage (North America, ANSI C84.1, 120 V base):** Range A service 114–126 V
  (±5%, confirmed in a USDA RUS bulletin reproducing the C84.1 table); Range A utilization minimum 110 V (secondary source); the utilization maximum and any lower non-lighting minimum (gated: unconfirmed, source is paywalled or blocked) — confirm in the current C84.1 Table 1. Range B is the short-term tolerance only.
- **Voltage (Europe, EN 50160 LV/MV):** ±10% of nominal for 95% of 10-minute means
  over a week (gated: unconfirmed, source is paywalled or blocked). Plant criteria are usually tighter, e.g. 0.95–1.05 pu at motor buses.
- **Thermal:** branches ≤ 100% of normal rating base case; ≤ emergency rating in
  contingencies. Transformers use nameplate top rating (e.g. ONAF) only if fans are proven.
- **Reactive:** generators should not sit at Q limits in the base case; look at
  where vars flow — large Q imports over long cables mean poor local compensation.
- **Losses:** compare I²R losses between options; they are often the economic decider.

## 5. Cases to run
Peak and light load (light load often gives *over*-voltage from cable charging and
capacitors), max and min generation, N-1 outages of every transformer and feeder,
tie open/closed, future load growth. Light-load + capacitors-on is the classic miss.

## 6. Gotchas
- Shunt capacitors' Q scales with V²; a "5 Mvar" bank gives 4.5 Mvar at 0.95 pu.
- Transformer tap sign conventions differ between tools (tap on HV vs LV side,
  % boost vs ratio); verify with a two-bus hand calculation.
- Angle spread > ~30° across a network usually signals a data error or a stressed corridor.

## Verify
- [ ] A hand calc of one feeder's voltage drop matches the solver within ~1%.
- [ ] Every island has exactly one slack; Q limits are enforced.
- [ ] Base and N-1 cases meet the stated voltage criterion and thermal ratings.
- [ ] Light-load over-voltage case has been run.
- [ ] Criteria source (ANSI C84.1, EN 50160, utility code, plant spec) is named in the report.
