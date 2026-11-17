---
id: engineering-technology.aerospace-engineering.aircraft-structures.damage-tolerance-part-25-571
name: damage-tolerance-part-25-571
category: engineering-technology
field: aerospace-engineering
product: aircraft-structures
tags: [aircraft-structures, fatigue, damage-tolerance, part-25-571, widespread-fatigue-damage, limit-of-validity, inspection-intervals, principal-structural-element]
level: advanced
status: verified
description: "Structure a damage-tolerance and fatigue evaluation under 25.571: principal structural elements, damage scenarios, inspection programme and limit of validity."
sources:
  - "14 CFR Part 25 section 25.571"
  - "FAA advisory circular 25.571 series (use the current revision)"
  - "EASA CS-25 section 25.571 and AMC"
  - "https://www.law.cornell.edu/cfr/text/14/25.571"
  - "eCFR 14 CFR 25.571, https://www.ecfr.gov/current/title-14/part-25/section-25.571"
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# Damage tolerance under 25.571

**Goal:** a programme showing catastrophic failure is avoided from fatigue, environmental and accidental damage. Practice guidance only; the rule text and AMC govern.

## Elements (current rule text to confirm)
- **Principal structural elements (PSE)** and other fatigue-critical structure identified (fuselage skins and frames, wing spars, skins, stringers, attach fittings, empennage).
- **Damage tolerance evaluation (25.571(b)):** the residual strength evaluation must show the remaining structure withstands static ultimate loads from the limit manoeuvre (25.337, 25.345), gust (25.341), rolling and yaw conditions up to `V_C`, pressurised-cabin cases (including 1.15 x maximum normal differential pressure alone) and landing-gear ground cases, with an extent of damage consistent with its initial detectability and growth. Inspection thresholds for single load path and some multiple-load-path structure are set from crack growth analyses and/or tests assuming an initial flaw of the maximum probable size (25.571(a)(3)). Safe-life scatter factors apply to the fatigue (safe-life) route of 25.571(c).
- **Widespread fatigue damage (WFD):** an LOV (a number of flight cycles or hours or both) must be established during which WFD is demonstrated not to occur, by full-scale fatigue test evidence. A type certificate may be issued before the test is finished if the Administrator approves a completion plan; the ALS then limits operation to 1/2 the cycles accumulated on the test article until the test is complete.
- **Discrete source damage (25.571(e)):** the airplane must complete a flight after likely damage from a 4 lb bird at `V_C` at sea level or 0.85 `V_C` at 8,000 ft (whichever is more critical), uncontained fan blade impact, uncontained engine failure, or uncontained high-energy rotating machinery failure; the damaged structure carries static loads (as ultimate) reasonably expected on that flight. Sonic fatigue is 25.571(d).
- **Outputs:** inspection programme items passed into the Airworthiness Limitations Section (ALS) of the instructions for continued airworthiness.

## Procedure
1. Select PSEs and critical locations from FE and test experience.
2. Define the stress spectrum and material data (see Paris skill).
3. Compute crack growth and residual strength curves; set thresholds and intervals with the agreed scatter factors.
4. Validate with full-scale fatigue test and teardown, which supports the LOV.
5. Document and submit to the authority.

## Gotchas
- Inspection capability (detection probability) is a programme assumption that must be demonstrated.
- Repairs and modifications need their own damage tolerance assessments.

## Verify
- [ ] Every PSE appears in the programme with threshold, interval and method.
