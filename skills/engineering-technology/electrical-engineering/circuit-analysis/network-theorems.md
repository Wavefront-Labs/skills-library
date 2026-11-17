---
id: engineering-technology.electrical-engineering.circuit-analysis.network-theorems
name: network-theorems
category: engineering-technology
field: electrical-engineering
product: circuit-analysis
tags: [circuit-analysis, electrical-engineering, kcl, kvl, max-power-transfer, mesh-analysis, network-theorems, nodal-analysis, norton-equivalent, supernode-handling, superposition, superposition-method, thevenin-equivalent]
level: intro
status: draft
description: "Solve linear circuits with nodal, mesh, superposition, Thevenin/Norton and maximum power transfer, with the dependent-source and supernode traps."
sources:
  - "https://www.ncees.org/engineering/fe/electrical-computer/"
  - "https://www.abet.org/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Network theorems: nodal, mesh, Thevenin/Norton, superposition

**Goal:** reduce a linear network to the smallest set of equations, and check the answer by a second method.

1. **Nodal (KCL):** pick a reference node, write `G v = i` (G = conductance matrix, diagonal = sum of conductances at the node, off-diagonal = minus shared conductance). Best when there are fewer nodes than meshes or many current sources.
2. **Supernode:** a voltage source between two non-reference nodes fixes their difference; merge the two nodes into one KCL equation and add `v_a - v_b = Vs`.
3. **Mesh (KVL):** best for planar circuits with many voltage sources. A current source shared by two meshes becomes a supermesh (one KVL around the outer loop plus a constraint `i_1 - i_2 = Is`).
4. **Superposition:** valid only for linear responses (voltage and current, never power). Turn off independent sources one at a time (voltage source = short, current source = open). Dependent sources always stay in.
5. **Thevenin:** `Voc` across the open terminals; `Rth = Voc/Isc`, or deactivate independent sources and look in. With dependent sources inside, apply a test source and take `Rth = vtest/itest`. Norton: `In = Isc`, same `Rth`.
6. **Maximum power transfer:** DC `RL = Rth`, `Pmax = Voc^2/(4 Rth)`; AC `ZL = conj(Zth)`. Maximum power is 50 % efficient at the source, so it is the wrong target for power delivery.

**Worked example:** 12 V source, 4 ohm in series, 12 ohm to ground, load across the 12 ohm. Voc = 12 x 12/16 = 9 V; Rth = 4 || 12 = 3 ohm; matched load 3 ohm gives Pmax = 81/12 = 6.75 W.

**Failure modes:** superposing power; shorting a dependent source; reversing source polarity in a supermesh; forgetting that Thevenin equivalents hide internal dissipation.

**Verify:** compute the load voltage by two different methods (for example nodal vs Thevenin) and confirm power balance (sum of source power equals sum of resistor power).

**Scope note:** Professional guidance only: design, selection, settings and sign-off belong to a qualified engineer or licensed electrician working to the code and standard editions adopted in the project jurisdiction. Standard clause numbers, limits and table values cited from memory are unconfirmed against the paywalled text (gated: unconfirmed, source is paywalled or blocked); worked arithmetic was recomputed.
