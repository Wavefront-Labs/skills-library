---
id: engineering-technology.chemical-engineering.process-control.decoupling-design
name: decoupling-design
category: engineering-technology
field: chemical-engineering
product: process-control
tags: [chemical-engineering, process-control, pc-multivariable-control, decoupling-design, decoupling, decoupler, interacting-loops, multivariable-control, static-decoupling, dynamic-decoupling, partial-decoupling, distillation-control]
level: advanced
status: gated
description: "Design static and dynamic decouplers for interacting 2 by 2 loops, assess sensitivity to model error, and compare with detuning and partial decoupling."
sources:
  - "Seborg Edgar Mellichamp and Doyle Process Dynamics and Control, Smith and Corripio Principles and Practice of Automatic Process Control, Luyben Process Modeling Simulation and Control, Skogestad Multivariable Feedback Control, ISA-18.2"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Decoupling design

**Goal:** reduce interaction so each loop can be tuned as if independent.

## Idea
For process y = G u with G 2 by 2, add compensators D so that G D is (nearly) diagonal.
- **Ideal (full) decoupler**: D = G^-1 G_diag, with G_diag the diagonal of G. Then each loop sees its own transfer function.
- **Static decoupler**: use the steady-state gain matrix G(0): D = G(0)^-1 diag(G(0)); simple, often enough when dynamics are similar.
- **Partial (one-way) decoupler**: compensate only the stronger interaction; robust and simple: d_21 = -G_21/G_22 and keep the other path.
- **Simplified decoupler**: use unit diagonal terms and cross terms D_12 = -G_12/G_11, D_21 = -G_21/G_22.

## Procedure
1. Identify the 2 by 2 transfer function matrix by step tests (see the identification skills).
2. Select the pairing by RGA.
3. Compute the decoupler terms; approximate them with lead-lag with delay (the ideal decoupler can be non-realisable if it needs negative delay).
4. Tune each loop on the diagonal model.
5. Test robustness: gain mismatch can degrade or destabilise the loops, particularly when the process is ill-conditioned (RGA elements much larger than 1 (gated: unconfirmed, source is paywalled or blocked)).

## Alternatives
Detune the loops (make one much slower than the other) to avoid interaction; use MPC when the system is larger or has constraints.

## Gotchas
- A decoupler for an ill-conditioned plant amplifies model error.
- When one manipulated variable saturates, decoupling is lost; the other loop sees the interaction.

## Verify
- [ ] Simulated step in one setpoint shows small effect on the other output (less than about 10%).
- [ ] Robustness test with perturbed gains stable.
