---
id: engineering-technology.chemical-engineering.process-design.equipment-cost-correlations-and-indexing
name: equipment-cost-correlations-and-indexing
category: engineering-technology
field: chemical-engineering
product: process-design
tags: [chemical-engineering, process-design, pd-capital-cost-estimation, equipment-cost-correlations-and-indexing, equipment-cost, cost-correlation, six-tenths-rule, cepci, cost-index, escalation, purchased-equipment-cost, capcost]
level: practitioner
status: gated
description: "Estimate purchased equipment cost from size correlations, scale with the six-tenths rule, escalate with a cost index (CEPCI) and apply material and pressure factors."
sources:
  - "Towler and Sinnott, Chemical Engineering Design; Turton et al., Analysis, Synthesis and Design of Chemical Processes; Peters, Timmerhaus and West, Plant Design and Economics (textbooks, method only)"
  - "Chemical Engineering magazine, Chemical Engineering Plant Cost Index (composite index built mostly from US BLS producer price indexes, premium subscription), https://www.chemengonline.com/pci-home"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Equipment cost correlations and index escalation

**Goal:** a purchased equipment cost for a given date and location that you can defend as screening-grade.

## Correlations
1. **Power-law scaling**: C2 = C1 (S2/S1)^n. The exponent n is often near 0.6 (six-tenths rule) but ranges widely by equipment type (about 0.4 to 0.9) (gated: unconfirmed, source is paywalled or blocked); use a tabulated exponent when available.
2. **Log-quadratic fits** (as in Turton et al.): log10 C_p0 = K1 + K2 log10 A + K3 (log10 A)^2 (gated: unconfirmed, source is paywalled or blocked) for base conditions (carbon steel, ambient pressure), with published constants valid over a stated size range. Do not extrapolate outside it.
3. **Adjustment factors**: pressure factor, material factor, and for module costing a bare-module factor.

## Escalation
Update a cost from year A to year B: C_B = C_A x (Index_B / Index_A). A common index is the Chemical Engineering Plant Cost Index (CEPCI) published in Chemical Engineering magazine; look up the current values yourself. Confirm the base year of each correlation (they are tied to the index at the time of publication).

## Procedure
1. Gather sizing data from the simulation and equipment list.
2. Apply the correlation inside its validity range; for out-of-range, split into parallel units or use vendor budget quotes.
3. Apply material and pressure factors.
4. Escalate to the estimate year; apply a location factor if needed.
5. Record source, base year, validity range for every cost.

## Gotchas
- Mixing correlations with different cost bases (equipment only versus installed).
- Using currency conversions for old data without index escalation.
- Cost correlations for large units often hide the need for multiple parallel trains above size limits.

## Verify
- [ ] Each item cost has source, year and range recorded.
- [ ] A vendor quote or recent project cost used to calibrate at least the largest items.
