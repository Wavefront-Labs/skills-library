---
id: engineering-technology.automotive-vehicle-engineering.crash-safety.b-pillar-and-roof-rail-design
name: b-pillar-and-roof-rail-design
category: engineering-technology
field: automotive-vehicle-engineering
product: crash-safety
tags: [b-pillar, roof-rail, roof-strength, fmvss-216, roof-crush, hot-stamped-pillar]
level: practitioner
status: gated
description: "Design the B-pillar and roof structure for side and roof-crush loads: hot-stamped pillars, tailored properties, strength-to-weight targets and checks."
sources:
  - "FMVSS 216 and IIHS roof strength protocol (nhtsa.gov, iihs.org); confirm current texts"
  - "Kramer, Passive Safety of Vehicles"
  - "https://www.law.cornell.edu/cfr/text/49/571.216"
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# B-pillar and roof rail design

1. Roles: B-pillar carries side-impact bending loads and contributes to roof strength; roof rails and A-pillars carry roof-crush loads; all connect to the door ring structure.
2. Roof crush tests: a plate is pushed into the roof at a slow rate; the metric is strength-to-weight ratio (peak force/vehicle weight) within a displacement limit (49 CFR 571.216 and 571.216a both limit plate travel to 127 mm). FMVSS 216 requires 1.5 times unloaded vehicle weight; the upgraded FMVSS 216a requires up to 3.0 times for GVWR of 2,722 kg (6,000 lb) or less and 1.5 times above that, and also limits head-form load to 222 N (checked against eCFR). IIHS rating thresholds: confirm in the current IIHS roof strength protocol (gated: unconfirmed, source is paywalled or blocked).
3. Materials: press-hardened boron steel in the B-pillar inner/outer, tailored by local tempering (softer zone near the bottom) for controlled deformation; ultra-high strength roof rails and header.
4. Joint design: pillar-to-roof and pillar-to-sill nodes with gussets; spot weld and weld-bonded flanges.
5. Mass: reinforce with minimal added mass using tailor-welded or tailor-rolled blanks.
6. Check for frontal and rollover load cases as well as side.
7. Verify with CAE of quasi-static roof crush and with the physical test.

**Gotchas:** stiff roof needs the A-pillar to carry load without buckling; glazing and sunroof frame matter.

## Verify
- [ ] Roof strength ratio from CAE exceeds the requirement at the specified displacement with margin.
- [ ] B-pillar intrusion in side tests within target.
