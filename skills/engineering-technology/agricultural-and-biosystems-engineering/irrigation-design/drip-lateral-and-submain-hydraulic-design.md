---
id: engineering-technology.agricultural-and-biosystems-engineering.irrigation-design.drip-lateral-and-submain-hydraulic-design
name: drip-lateral-and-submain-hydraulic-design
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: irrigation-design
tags: [agricultural-and-biosystems-engineering, irrigation-design, lateral-hydraulics, drip-design, micro-irrigation, christiansen-factor, friction-loss, submain-design, pressure-variation]
level: practitioner
status: gated
description: "Design drip laterals and submains within a pressure-variation budget: Hazen-Williams or Blasius friction, Christiansen F, slope effects and the allowable head difference split."
sources:
  - "Keller & Bliesner, Sprinkle and Trickle Irrigation"
  - "Hoffman et al., Design and Operation of Farm Irrigation Systems (ASABE)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Drip lateral and submain hydraulic design

**Goal:** keep flow variation within about 10 percent across a block with the smallest pipe cost.

## Budget
For emitters with exponent x, a flow variation limit `dq/q` gives allowable head variation `dH/H = (dq/q) / x`; for turbulent emitters, 10 percent flow variation allows about 20 percent head variation (0.1 / 0.5, linearised). The head variation budget covers both lateral and submain (manifold), plus elevation changes. A common split gives the lateral a slightly larger part (about 55 percent in a textbook example (gated: unconfirmed, source is paywalled or blocked)), subject to cost optimisation. For PC emitters, the pressure range is set by the maker.

## Friction loss
- Use Darcy-Weisbach with Blasius for smooth PE pipe at moderate Re, or Hazen-Williams with C of roughly 140-150 for PE (gated: unconfirmed, source is paywalled or blocked); PE tube has a variable inner diameter, so use the maker's actual ID.
- Multiple-outlet reduction (Christiansen): `F = 1/(m+1) + 1/(2N) + sqrt(m-1)/(6 N^2)`, with m = 1.75 for Blasius or 1.852 for Hazen-Williams; F is about 0.36 for many outlets with m = 1.75 and about 0.35 with m = 1.852 (formula checked against a direct sum over N outlets; computed). Friction over the lateral = F x (loss if full flow ran the whole length).
- Add minor losses of emitter barbs for online emitters.

## Slope
Uphill adds head loss; downhill adds head gain; contour laterals are best. Use the average head and extremes for minimum and maximum pressure, and check both ends of the block.

## Submain
Design with a tapered diameter per section for slopes and flow; compute hydraulic gradient section by section; ensure the first and last laterals have the same average pressure within budget.

## Gotchas
- Laterals longer than the design limit cause tail-end starvation.
- Do not forget the filter and the valve pressure losses at the head of the block.

## Verify
- [ ] Spreadsheet or software computes pressure at every lateral inlet and end.
- [ ] Field gauge readings at head and tail match design within 10 percent.
