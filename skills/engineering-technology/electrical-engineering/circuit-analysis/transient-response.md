---
id: engineering-technology.electrical-engineering.circuit-analysis.transient-response
name: transient-response
category: engineering-technology
field: electrical-engineering
product: circuit-analysis
tags: [circuit-analysis, damping, electrical-engineering, laplace-circuit-analysis, laplace-transform, natural-and-step-response, rlc-circuit, time-constant, transient-response]
level: practitioner
status: draft
description: "Solve first-order and RLC transients, classify damping, and use Laplace element models for switching events."
sources:
  - "https://www.ncees.org/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Transient response of RL, RC and RLC circuits

- **First order:** `x(t) = x_inf + (x_0 - x_inf) e^(-t/tau)`; `tau = L/R` or `RC`. Inductor current and capacitor voltage cannot jump; after 5 tau the response is within about 0.7 %.
- **Series RLC:** `alpha = R/(2L)`, `w0 = 1/sqrt(LC)`. Overdamped if `alpha > w0` (two real roots), critical if equal, underdamped if `alpha < w0` with `wd = sqrt(w0^2 - alpha^2)`. Parallel RLC: `alpha = 1/(2RC)`.
- **Example:** R = 10 ohm, L = 10 mH, C = 100 uF: `alpha = 500`, `w0 = 1000`, so underdamped with `wd = 866 rad/s`.
- **Laplace models:** resistor `R`; inductor `sL` in series with a source `L i0` (opposing the initial current direction convention you chose); capacitor `1/(sC)` in series with `v0/s`. Solve algebraically, then partial-fraction to time domain.
- **Switching surge awareness:** an underdamped LC switch-on can overshoot toward twice the step; this is why capacitor energisation needs inrush control.

**Verify:** check initial and final values by inspection (inductor short and capacitor open at DC steady state), then simulate.

**Scope note:** Professional guidance only: design, selection, settings and sign-off belong to a qualified engineer or licensed electrician working to the code and standard editions adopted in the project jurisdiction. Standard clause numbers, limits and table values cited from memory are unconfirmed against the paywalled text (gated: unconfirmed, source is paywalled or blocked); worked arithmetic was recomputed.
