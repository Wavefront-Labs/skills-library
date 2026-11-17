---
id: engineering-technology.chemical-engineering.process-control.relative-gain-array-pairing
name: relative-gain-array-pairing
category: engineering-technology
field: chemical-engineering
product: process-control
tags: [chemical-engineering, process-control, pc-multivariable-control, relative-gain-array-pairing, relative-gain-array, rga, loop-pairing, interaction, bristol, steady-state-gain-matrix, multivariable-control, pairing-selection]
level: advanced
status: verified
description: "Compute the relative gain array from steady-state gains to choose input-output pairings, avoid negative-gain pairings, and judge interaction severity."
sources:
  - "Bristol, E.H. (1966) On a new measure of interaction for multivariable process control, IEEE Trans. Autom. Control 11(1):133-134, https://doi.org/10.1109/TAC.1966.1098266"
  - "Niederlinski, A. (1971) A heuristic approach to the design of linear multivariable interacting control systems, Automatica 7(6):691-701, https://doi.org/10.1016/0005-1098(71)90007-0"
  - "Seborg, Edgar, Mellichamp and Doyle, Process Dynamics and Control (textbook, method only)"
  - "Worked example recomputed with numpy: RGA diagonal 2.2857, off-diagonal -1.2857, 1/lambda = 0.4375"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Relative gain array pairing

**Goal:** choose which manipulated variable controls which output, and gauge loop interaction.

## Definition
For a square steady-state gain matrix G, RGA = G .* (G^-1)^T (element-wise product). For a 2 by 2 system: lambda_11 = 1/(1 - K_12 K_21/(K_11 K_22)); lambda_12 = 1 - lambda_11. Rows and columns sum to one.

## Interpretation
- lambda_ij = 1: no interaction on that pairing: ideal.
- Closing the other loop changes the effective gain of the paired loop from K to K/lambda_ij. For 0 < lambda_ij < 1 the gain rises; for lambda_ij > 1 it falls. Values close to 1 are good; values much greater than 1 (above about 5 to 10) mean strong interaction, sensitivity to model error and difficult control.
- lambda_ij < 0: the sign of the gain reverses when the other loop closes; **avoid** such pairings (instability on loop failure).
- Rule: pair on elements positive and as close to 1 as possible.

## Procedure
1. Obtain steady-state gains from step tests or a simulator (for a ratio-type model scale to consistent units).
2. Compute RGA; with more than two variables use the matrix formula.
3. Select a pairing that avoids negative elements, and check the Niederlinski index (NI < 0 means the paired decentralised system with integral action is unstable, so NI > 0 is a necessary condition for stability; Niederlinski 1971).
4. Consider dynamics: the RGA at the crossover frequency is more relevant than the steady state; if the steady state and dynamic RGA disagree, rely on the dynamic.
5. If no good pairing exists, use decoupling or MPC.

## Example
G = [[2, 1.5], [1.5, 2]]: lambda_11 = 1/(1 - (1.5 x 1.5)/(2 x 2)) = 1/(1 - 0.5625) = 2.29. The diagonal pairing is acceptable but interactive: closing the second loop cuts the first loop's gain to 1/2.29, about 44% of its open-loop value, so tune with the other loop closed.

## Gotchas
- The RGA is independent of input and output scaling, but it is sensitive to errors in the gains, especially for ill-conditioned plants.
- Integrating processes need a modified RGA.

## Verify
- [ ] Pairing has positive RGA elements and a positive NI.
- [ ] Interaction tested by closing the loops sequentially in a simulation.
