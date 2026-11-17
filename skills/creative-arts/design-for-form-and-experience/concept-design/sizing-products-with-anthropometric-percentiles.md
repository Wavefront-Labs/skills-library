---
id: creative-arts.design-for-form-and-experience.concept-design.sizing-products-with-anthropometric-percentiles
name: sizing-products-with-anthropometric-percentiles
category: creative-arts
field: design-for-form-and-experience
product: concept-design
tags: [human-factors, ergonomics, anthropometrics, percentile-design, 5th-percentile, 95th-percentile, design-for-adjustability, dreyfuss, product-design]
level: practitioner
status: draft
description: "Size a product to its users with anthropometric data: choose the right percentile per dimension, design for extremes or adjustability, add clothing allowances."
sources:
  - "Henry Dreyfuss Associates, The Measure of Man and Woman (Wiley)"
  - "ANSUR II US Army anthropometric survey (openlab.psu.edu/ansur2)"
  - "ISO 7250-1 Basic human body measurements for technological design"
  - "NASAD Handbook, industrial design human factors competency"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Anthropometric percentiles in sizing

**Goal:** every critical dimension fits the people who will use it, chosen by rule rather than
"average person" guessing. There is no average person; someone at the 50th percentile in
stature is rarely 50th in arm length.

## Steps
1. **Define the user population:** country, age range, sex mix, special groups (children,
   older adults, gloved workers). Pick a data set that matches: ANSUR II (military, fit adults),
   national surveys, Dreyfuss charts, ISO 7250 compilations.
2. **List critical dimensions** and classify each:
| Type | Design for | Example |
|---|---|---|
| Clearance (must fit the biggest) | 95th or 99th percentile large user | Doorway height, handle opening for gloved hands, legroom |
| Reach (must fit the smallest) | 5th percentile small user | Reach to a control, button force, grip span on a trigger |
| Adjustable | 5th female to 95th male range | Seat height, monitor arm, strap length |
| Comfort / average-use | 50th, then check extremes | Mouse size, non-critical handle diameter |
3. **Add allowances:** clothing and shoes (shoes add about 25-40 mm to stature), gloves (add
   10-20 mm to hand thickness), posture slump, movement envelope.
4. **Check combinations:** a 5th percentile reach and a 95th percentile clearance in the same
   layout can conflict; resolve with adjustability or separate variants (S/M/L).
5. **Validate with people:** a sizing mockup tried by users at both ends of the range.

## Gotchas
- Percentiles do not add: summing 95th percentile segments gives a body nobody has.
- Older data sets underestimate today's body sizes; check survey dates.
- For safety (guards, openings fingers must not reach through) use standards such as ISO 13857,
  not general survey data.

## Verify
Every critical dimension has a recorded percentile, data source and allowance; mockup tests
include users near both target extremes.
