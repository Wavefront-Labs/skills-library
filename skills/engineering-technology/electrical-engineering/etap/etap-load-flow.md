---
id: engineering-technology.electrical-engineering.etap.etap-load-flow
name: etap-load-flow
category: engineering-technology
field: electrical-engineering
product: etap
tags: [electrical-engineering, etap, etap-load-flow, etap-load-flow-alerts, etap-load-flow-methods, etap-voltage-profile, load-flow-study]
level: practitioner
status: draft
description: "Run an ETAP load-flow study: solution method, loading categories, voltage profile and alert review."
sources:
  - "https://etap.com/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# ETAP load-flow study

1. **Method:** choose among the offered iterative solvers (Newton-Raphson, fast-decoupled, accelerated Gauss-Seidel) in the study case; Newton-Raphson is the usual default for convergence on meshed networks; adjust iterations and precision if it does not converge.
2. **Loading category and diversity:** pick the loading category (design, normal, emergency) and apply global load diversity factors only when justified.
3. **Source modelling:** swing (slack) bus for the utility, voltage-controlled buses for generators, and tap-changer or regulator control with target voltage and band.
4. **Alerts:** set critical and marginal thresholds for overvoltage and undervoltage (for example 105 and 95 percent) and for equipment loading (for example 100 and 95 percent).
5. **Outputs:** bus voltages, branch flows and losses, power factor at the utility connection, and voltage drops to the farthest motors (check starting limits in a separate motor-starting study).
6. Use the capacitor sizing and optimal capacitor placement tools only after confirming the harmonics implications.

**Tool-detail caveat:** menu names and report fields below are described from general ETAP practice and the ETAP documentation structure; confirm exact labels and options in the installed ETAP version's help (status draft, tool behaviour not re-run for this entry).

**Verify:** total generation equals load plus losses in the summary; check that the swing bus real power is within its rating.

**Scope note:** Professional guidance only: design, selection, settings and sign-off belong to a qualified engineer or licensed electrician working to the code and standard editions adopted in the project jurisdiction. Standard clause numbers, limits and table values cited from memory are unconfirmed against the paywalled text (gated: unconfirmed, source is paywalled or blocked); worked arithmetic was recomputed.
