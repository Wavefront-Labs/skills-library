---
id: engineering-technology.agricultural-and-biosystems-engineering.farm-machinery-design.implement-draft-prediction-asabe
name: implement-draft-prediction-asabe
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: farm-machinery-design
tags: [agricultural-and-biosystems-engineering, farm-machinery-design, draft-prediction, tillage, implement-draft, asabe-d497, specific-draft, soil-texture-index]
level: practitioner
status: verified
description: "Predict implement draft from tool width, depth and speed using the ASABE D497 draft equation, then size tractor power and check against a drawbar test."
sources:
  - "University of Arizona Cooperative Extension, agricultural machinery management (https://cales.arizona.edu/crops/equipment/agmachinerymgt.html)"
  - "ASABE D497 Agricultural Machinery Management Data (paywalled; index at https://www.asabe.org)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Implement draft prediction (ASABE D497 form)

**Goal:** a first estimate of the pull a tillage tool needs before buying or matching a tractor.

## Equation form
ASABE D497 gives draft in a quadratic-in-speed form:

`D = F_i x (A + B S + C S^2) x W x T`

where D is draft (N), F_i a soil texture adjustment indexed i = 1 for fine, 2 for medium, 3 for coarse (University of Arizona extension; other papers use a different scale, so take the values from the standard), S speed (km/h), W width or number of units, T working depth (cm for depth-based tools), and A, B, C coefficients tabulated for each implement type. Coefficients are in the current D497 data table; use them from the standard. The draft depends strongly on soil moisture and compaction, so apply the standard's note that it is a typical value, not a guarantee.

## Use
1. Pick the tool row, soil texture, planned speed, width and depth.
2. Compute D, then drawbar power `P = D x S / 3.6` (D in kN, S in km/h gives kW). Check (computed): D = 50 kN at 7 km/h gives 50 x 7 / 3.6 = 97.2 kW.
3. Required engine power from drawbar power divided by tractive efficiency and transmission efficiency (see drawbar skill).
4. Add 10-20 percent reserve for hard spots. Verify against a local trial pull using a load cell or tractor fuel use.

## Gotchas
- Depth has a nonlinear effect; use the depth the tool will actually reach, not the setting.
- Worn shares and tines can raise draft substantially.
- Do not compare unlike units (metric versus US) without converting coefficients.

## Verify
- [ ] Predicted and measured draft agree within about 25 percent; if not, adjust for soil and wear.
