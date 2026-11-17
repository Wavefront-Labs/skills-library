---
id: engineering-technology.aerospace-engineering.spacecraft-systems-design.radiation-total-ionizing-dose
name: radiation-total-ionizing-dose
category: engineering-technology
field: aerospace-engineering
product: spacecraft-systems-design
tags: [radiation-tid, total-ionizing-dose, radiation-hardness, shielding, radiation-design-margin, space-environment]
level: practitioner
status: verified
description: "Estimate total ionizing dose behind shielding, apply radiation design margin, choose parts and plan TID testing and ELDRS checks."
sources:
  - "ESA ECSS-E-ST-10-04C (space environment)"
  - "MIL-STD-883 Method 1019"
  - "ESCC 22900"
  - "NASA radiation effects guidance"
  - "ESCC 22900 total dose steady-state irradiation test method (ESCIES): https://escies.org"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Radiation total dose

**Goal:** parts survive the mission dose with margin.

## Environment
Trapped electrons and protons (radiation belts), solar energetic particles and galactic cosmic rays. Dose depends on orbit and time in the belts (MEO and GEO are severe for electrons; high LEO crosses the South Atlantic Anomaly).

## Procedure
1. Compute the dose-depth curve for the orbit and duration with a space environment tool (for example ESA's SPENVIS or comparable tools) using the AE9/AP9 or older AE8/AP8 trapped models.
2. Determine shielding at each part: spacecraft structure, box walls, and local shielding; use sector analysis or ray tracing.
3. Dose at the part, in krad (Si) (or gray); apply the radiation design margin (a factor of 2 is a common programme requirement (gated: unconfirmed, source is paywalled or blocked); the radiation design margin is defined in ECSS-E-ST-10-12, use your programme's).
4. Compare with part TID capability from datasheets, test reports or a lot-specific test.
5. Test: cobalt-60 gamma source per MIL-STD-883 Method 1019 (microcircuit ionizing radiation total dose test) or ESCC Basic Specification 22900 (total dose steady-state irradiation test method); bipolar parts may show enhanced low dose rate sensitivity (ELDRS) so test at low dose rate or use the specified protocol.
6. Mitigate: spot shielding, part choice, derating, circuit design.

## Gotchas
- Parts from different wafer lots can differ; lot qualification matters.
- Total dose is one effect; single-event effects need separate analysis.
- Commercial parts need test or heritage data for the specific lot; datasheet "radiation tolerant" claims vary.

## Verify
- [ ] Every part's tested or rated TID is at least the mission dose times the design margin.
