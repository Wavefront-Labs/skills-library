---
id: engineering-technology.chemical-engineering.heat-exchanger-design.tema-type-selection
name: tema-type-selection
category: engineering-technology
field: chemical-engineering
product: heat-exchanger-design
tags: [chemical-engineering, heat-exchanger-design, hx-shell-and-tube-selection, tema-type-selection, tema, shell-and-tube, floating-head, fixed-tubesheet, u-tube, bem, aes, exchanger-selection, tema-classes]
level: practitioner
status: gated
description: "Choose TEMA shell-and-tube types (front head, shell, rear head letters), such as AES, BEM, AEU, from fouling, thermal expansion, cleaning and cost considerations."
sources:
  - "Kern Process Heat Transfer, Perry Handbook heat transfer section, TEMA Standards, Heat Exchanger Design Handbook (HEDH), Kemp Pinch Analysis and Process Integration, Smith Chemical Process Design and Integration"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TEMA type selection

**Goal:** the TEMA designation (three letters) that suits the duty.

## Letter code (TEMA standards; confirm against the current edition (gated: unconfirmed, source is paywalled or blocked))
- **Front head**: A (channel with removable cover), B (bonnet), C and N (channel integral with tubesheet), D (high pressure closure).
- **Shell**: E (one pass), F (two pass with longitudinal baffle), G and H (split flow variants), J (divided flow), K (kettle reboiler), X (cross flow).
- **Rear head**: L, M, N (fixed tubesheet types), P (outside packed floating head), S (floating head with backing device), T (pull-through floating head), U (U-tube bundle), W (externally sealed floating tubesheet).

## Typical choices
| Need | Common type |
|---|---|
| Clean fluids, small temperature difference, lowest cost | BEM (fixed tubesheet) |
| Fouling on shell side needing bundle removal | AES or AET (floating head) |
| Large thermal expansion, clean tube side | BEU or AEU (U-tube; tube side must be clean because cleaning bends is difficult) |
| Reboiler with vapour disengagement | AKT or similar kettle (K shell) |

## Decision criteria
1. **Thermal expansion difference** between shell and tubes: fixed tubesheet needs an expansion joint if the difference is large; otherwise floating head or U-tube.
2. **Cleaning**: shell side can be cleaned only if the bundle is removable and the layout is square; tube side by mechanical cleaning needs removable covers (A head) and straight tubes.
3. **Pressure and hazard**: high pressure or toxic service favours designs with fewer gasketed joints and a stronger code class.
4. **Cost**: fixed tubesheet cheapest, U-tube next, floating head highest.
5. **TEMA class** (R for severe petroleum and related service, C for moderate commercial, B for chemical process): choose by the client or code requirement.

## Gotchas
- A shell-side fouling fluid with a U-tube bundle is difficult to clean; consider the allocation first.
- Fixed tubesheet exchangers cannot be inspected or cleaned on the shell side without opening a bypass; plan for spare capacity.

## Verify
- [ ] TEMA letters justified in the data sheet with cleaning and expansion reasoning.
- [ ] Applicable code and TEMA edition and class recorded.
