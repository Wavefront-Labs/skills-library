---
id: engineering-technology.electrical-engineering.power-system-analysis.voltage-regulation-control
name: voltage-regulation-control
category: engineering-technology
field: electrical-engineering
product: power-system-analysis
tags: [electrical-engineering, on-load-tap-changer, power-system-analysis, pv-curve, reactive-compensation-siting, shunt-reactor, statcom, tap-changer, voltage-regulation, voltage-regulation-control, voltage-stability-pv-curve]
level: practitioner
status: draft
description: "Plan voltage control with tap changers, shunt and series compensation, and read PV curves for voltage stability margin."
sources:
  - "https://standards.ieee.org/"
  - "https://www.ncees.org/engineering/pe/electrical-computer/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Voltage regulation and reactive power control

1. **Approximate drop:** `dV ~ (R P + X Q) / V` per unit. On transmission X dominates so Q controls voltage; on distribution R is significant so P also matters.
2. **On-load tap changer:** typical regulation is plus or minus 10 percent in 16 steps of 0.625 percent (confirm against the transformer nameplate); control uses a bandwidth around the setpoint and a time delay longer than the downstream regulator delay, with line-drop compensation optional.
3. **Reactive support:** shunt capacitor banks raise voltage, shunt reactors lower it, STATCOM and SVC give continuous control; place devices where voltage drops are largest, checking switching transients.
4. **PV curve:** plot bus voltage against transfer power while holding power factor; the nose is the maximum loadability. Operate with a margin (utilities specify a percent of nose MW). Past the nose, voltage collapses.
5. Reactive power capability limits (generator capability curves, inverter limits) bound the available control.

**Verify:** run a load-flow at peak and light load and confirm voltages sit in the planning range (often 0.95 to 1.05 pu) for normal and N-1 conditions.

**Scope note:** Professional guidance only: design, selection, settings and sign-off belong to a qualified engineer or licensed electrician working to the code and standard editions adopted in the project jurisdiction. Standard clause numbers, limits and table values cited from memory are unconfirmed against the paywalled text (gated: unconfirmed, source is paywalled or blocked); worked arithmetic was recomputed.
