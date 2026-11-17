---
id: engineering-technology.aerospace-engineering.aircraft-structures.limit-and-ultimate-load-factors
name: limit-and-ultimate-load-factors
category: engineering-technology
field: aerospace-engineering
product: aircraft-structures
tags: [limit-ultimate, limit-load, ultimate-load, factor-of-safety, structural-loads, part-25]
level: practitioner
status: verified
description: "Apply limit and ultimate load definitions and the 1.5 factor of safety in transport-category structural sizing, with fitting and special factors, and defer to the regulator."
sources:
  - "FAA 14 CFR Part 25"
  - "EASA CS-25"
  - "Niu, Airframe Structural Design"
  - "eCFR 14 CFR 25.303 and 25.305, https://www.ecfr.gov/current/title-14/part-25/subpart-C"
  - "eCFR 14 CFR 25.625, https://www.ecfr.gov/current/title-14/part-25/section-25.625"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Limit and ultimate loads

**Goal:** size structure to the right load level and show margins at both.

## Definitions (transport category)
- **Limit load**: the maximum load expected in service. Structure must carry limit load without detrimental permanent deformation, with deformation not interfering with safe operation.
- **Ultimate load**: limit load multiplied by a factor of safety, normally 1.5 unless the rules say otherwise. Structure must carry ultimate load without failure for at least 3 seconds (25.305(b)); the 3-second limit does not apply when strength is shown by dynamic tests simulating actual load conditions. 25.303: the 1.5 factor applies to prescribed limit loads that are external loads, and need not be applied when a condition is prescribed directly in ultimate loads.
- These come from the strength requirements in 14 CFR 25.301 to 25.307 (checked against eCFR 25.303, 25.305, 25.307, 25.625) and the matching CS-25 paragraphs. Always read the current text of the rule applying to your certification basis.

## Practice
1. Compute limit loads from the V-n and gust envelopes and the ground and landing cases (see vn-manoeuvre-envelope, gust-load-factors).
2. Size for ultimate: `MS = (allowable / (1.5 * limit stress)) - 1` with ultimate allowables; check yield at limit with yield allowables: `MS = (Fty / limit stress) - 1`.
3. Apply special factors where the rules require them, for example the 25.625 fitting factor of at least 1.15 on the fitting, its attachment and the bearing on the joined members when the fitting is not proven by limit and ultimate load tests (no factor for joints under approved practices with comprehensive test data). Confirm the other special factors in subpart D for your structure.
4. Report the minimum margin per component and the governing load case.
5. Keep limit and ultimate checks distinct: stability (buckling) is usually checked at ultimate; deformation and stiffness requirements at limit.

## Gotchas
- Mixing a limit stress with an ultimate allowable gives a hidden 1.5 error.
- Thermal and pressurisation loads have their own combination rules; do not skip them.
- Compliance is shown to the airworthiness authority; this skill is working practice, not the rule.

## Verify
- [ ] Each margin states which load level, which allowable and which factor it used.
