---
id: engineering-technology.chemical-engineering.aspen.radfrac-setup-and-specifications
name: radfrac-setup-and-specifications
category: engineering-technology
field: chemical-engineering
product: aspen
tags: [chemical-engineering, aspen, aspen-column-simulation, radfrac-setup-and-specifications, radfrac, distillation-simulation, column-specification, aspen-plus, reflux-ratio, design-spec, rigorous-distillation]
level: practitioner
status: gated
description: "Set up RadFrac in Aspen Plus: stages, condenser and reboiler types, feed stages, operating specs, pressure profile and valid phases, in a convergence-friendly order."
sources:
  - "Aspen Plus and Aspen HYSYS user guides and help (AspenTech), Seider et al. Product and Process Design Principles"
  - "https://www.aiche.org"
  - "AspenTech Aspen Plus certification study guide AT-05198 (learning objectives, aspentech.com)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RadFrac setup and specification choices

**Goal:** a RadFrac column that solves on the first or second try and means what you intended.

## Order of work
1. Start from a shortcut result (see `engineering-technology.chemical-engineering.separation-processes.fenske-minimum-stages`): number of stages, feed stage, reflux ratio.
2. **Configuration**: calculation type Equilibrium; stages; condenser (Total, Partial-Vapor, Partial-Vapor-Liquid or None); reboiler (Kettle, Thermosiphon, or None for steam-stripped columns) (gated: unconfirmed, source is paywalled or blocked); valid phases (Vapor-Liquid, or Vapor-Liquid-Liquid for heterogeneous); convergence setting Standard to begin.
3. **Two operating specs**: the pair controls the degrees of freedom. Typical: distillate rate (or distillate-to-feed ratio) plus reflux ratio. Avoid specifying a composition spec until the column solves with simple specs.
4. **Streams**: feed stage and convention (Above-Stage or On-Stage; both confirmed in AspenTech's study guide); product draws from stages.
5. **Pressure**: top pressure and per-stage or section drop; use realistic values (about 0.007 to 0.01 bar per tray as a first guess (gated: unconfirmed, source is paywalled or blocked); check later from hydraulics).
6. **Design specs and Vary** (composition or recovery specs) added after the base case solves.
7. **Efficiency**: set Murphree or vaporisation efficiencies only after the stage-count design is set; otherwise keep 100% theoretical stages.

## Typical specs
Distillate purity: Design spec of mole fraction in distillate, vary reflux ratio (or distillate rate). Bottoms purity: bottoms rate varies. Both purities specified need both reflux and rate varied.

## Gotchas
- Over-specifying (three specs) gives a block error; under-specifying gives no solution.
- A purity spec that is infeasible at the stage count shows as the Vary hitting its bounds; extend the bounds or add stages.

## Verify
- [ ] Block converged with no warnings; mass balance closes.
- [ ] Reboiler and condenser duty plausible versus shortcut result.
- [ ] Temperature and composition profiles are smooth.
