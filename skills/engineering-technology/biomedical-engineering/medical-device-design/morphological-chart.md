---
id: engineering-technology.biomedical-engineering.medical-device-design.morphological-chart
name: morphological-chart
category: engineering-technology
field: biomedical-engineering
product: medical-device-design
tags: [morphological-chart, concept-selection, concept-generation, function-decomposition, systematic-design, zwicky-box]
level: practitioner
status: draft
description: "Generate device concepts with a morphological chart: decompose functions, list solution options per function, combine them into coherent concepts and prune with constraints."
sources: ["Pahl and Beitz, Engineering Design: A Systematic Approach", "Ulrich and Eppinger, Product Design and Development (concept generation chapter)", "Zenios et al., Biodesign: The Process of Innovating Medical Technologies"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Morphological chart

**Goal:** explore the design space systematically before choosing, so the first idea does not dominate.

## Steps
1. **Decompose functions** from the design inputs: for a drug-delivery pen, for example, "contain drug", "set dose", "drive plunger", "indicate dose", "protect needle", "provide feedback".
2. **List solution principles** for each function (3-6 each), including unconventional ones: mechanical spring, gas, electric motor, manual push; clutch, ratchet, screw; audible, tactile, visual feedback.
3. **Draw the chart:** rows are functions, columns are options.
4. **Combine one option per function** into 5-10 concept paths; draw them as lines through the chart. Use at least one safe baseline and one aggressive concept.
5. **Check compatibility:** some pairings are impossible (power source versus drive); remove incoherent combinations.
6. **Sketch** each concept (block diagram, a rough layout) so the team understands it.
7. **Select** with a Pugh or weighted matrix (see pugh-concept-matrix and weighted-decision-matrix).

## Tips
- Brainstorm options for each function separately, with TRIZ or biomimicry for stuck functions.
- Keep medical context: sterilisation, biocompatibility and failure modes constrain options early; note them in the chart.
- Record rejected concepts and the reason in the design history.

## Verify
- [ ] Each function has several options, not one.
- [ ] Concept combinations are coherent and sketched.
- [ ] Rejection reasons are written for traceability.
