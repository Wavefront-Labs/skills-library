---
id: engineering-technology.chemical-engineering.process-control.ziegler-nichols-and-relay-autotune
name: ziegler-nichols-and-relay-autotune
category: engineering-technology
field: chemical-engineering
product: process-control
tags: [chemical-engineering, process-control, pc-pid-tuning, ziegler-nichols-and-relay-autotune, ziegler-nichols, ultimate-gain, ultimate-period, relay-autotune, astrom-hagglund, reaction-curve, pid-tuning, quarter-decay, autotuner]
level: practitioner
status: gated
description: "Use Ziegler-Nichols open- and closed-loop rules and relay autotuning to get starting PID settings, with their known aggressiveness and safe application limits."
sources:
  - "Ziegler, J.G. and Nichols, N.B. (1942) Optimum settings for automatic controllers, Trans. ASME 64:759-768"
  - "Astrom, K.J. and Hagglund, T. (1984) Automatic tuning of simple regulators with specifications on phase and amplitude margins, Automatica 20(5):645-651, https://doi.org/10.1016/0005-1098(84)90014-1"
  - "Tyreus, B.D. and Luyben, W.L. (1992) Tuning PI controllers for integrator/dead time processes, Ind. Eng. Chem. Res. 31(11):2625-2628, https://doi.org/10.1021/ie00011a029"
  - "https://pages.mtu.edu/~tbco/cm416/zn.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ziegler-Nichols and relay autotune

**Goal:** a quick tuning start where little modelling is possible, with awareness of the risks.

## Ziegler-Nichols closed-loop (ultimate gain) method
1. With the controller in P-only, raise Kc until sustained oscillation of constant amplitude occurs at the ultimate gain Ku and ultimate period Pu. (Do this only where the process can tolerate it; many plants cannot.)
2. Settings: P: Kc = 0.5 Ku; PI: Kc = 0.45 Ku, Ti = Pu/1.2; PID: Kc = 0.6 Ku, Ti = Pu/2, Td = Pu/8.

## Open-loop (reaction curve) version
From an FOPDT fit (K, tau, theta): PI: Kc = 0.9 tau/(K theta), Ti = 3.33 theta; PID: Kc = 1.2 tau/(K theta), Ti = 2 theta, Td = 0.5 theta (gated: unconfirmed, source is paywalled or blocked).

## Relay autotune (Astrom-Hagglund)
1. Replace the controller by a relay of amplitude d around the operating output; the loop develops a limit cycle of amplitude a and period Pu.
2. Ultimate gain Ku = 4d/(pi a); then use the ZN or a modified table (Tyreus-Luyben gives Kc = Ku/3.2, Ti = 2.2 Pu for PI with less oscillation; Ku/2.2 is the Ziegler-Nichols PI gain).
3. The relay keeps the amplitude bounded, so it is safer than pushing gain to instability.

## Cautions
- ZN settings aim at quarter-amplitude decay, too oscillatory for most process loops; reduce Kc by 30 to 50% (gated: unconfirmed, source is paywalled or blocked) or use Tyreus-Luyben or IMC rules for general use.
- Do not apply the ultimate-gain test to safety-critical or constraint-bound loops.
- Valve stiction produces limit cycles that look like relay cycles; confirm the valve first.

## Gotchas
- Noise and deadzone distort Pu; average over several cycles.
- Slow lag-dominant processes take hours to test; use a model-based method.

## Verify
- [ ] Closed-loop response with the derated settings is acceptable (overshoot, decay ratio).
- [ ] Settings recorded with the test data in the loop file.
