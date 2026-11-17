---
id: engineering-technology.automotive-vehicle-engineering.crash-safety.iihs-small-overlap-test
name: iihs-small-overlap-test
category: engineering-technology
field: automotive-vehicle-engineering
product: crash-safety
tags: [iihs-small-overlap, small-overlap, iihs, narrow-offset, a-pillar-intrusion, wheel-intrusion]
level: practitioner
status: gated
description: "Understand the IIHS small overlap frontal test: 25% overlap rigid barrier, structural goals, wheel and hinge-pillar intrusion and restraint kinematics."
sources:
  - "IIHS crash test protocol documents (iihs.org); confirm the current protocol version"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# IIHS small overlap test

1. Configuration: vehicle at 64.4 +/- 1 km/h (40 mph) hits a rigid barrier with 25 +/- 1% overlap (IIHS small overlap test protocol, Version VII, May 2021, fetched; driver-side, with a passenger-side evaluation also in the protocol and the combined rating taking the lower). The barrier edge misses the main longitudinal rails, so loads go through wheel, hinge pillar and A-pillar.
2. (Rating-category description from memory (gated: unconfirmed, source is paywalled or blocked).) Ratings assess structure (intrusion measurements in the footwell, instrument panel and door/hinge-pillar), occupant injury measures from the dummy, and restraints/kinematics (dummy movement, airbag effectiveness). Confirm the current measurement points and rating thresholds in the protocol.
3. Structural strategies: extend or strengthen the front rail with an outrigger or shotgun load path to engage the barrier; deflect the vehicle laterally away from the barrier; strong hinge pillar, rocker, and a strong A-pillar/door beam; wheel strut and lower arm designed to break away without pushing the wheel into the footwell.
4. Restraints: curtain/side airbags and larger driver airbag covering lateral motion; belt pretensioning tuned for lateral kinematics.
5. CAE: simulate with a barrier model and verify with partial prototypes; check sensitivity to barrier edge position.

**Gotchas:** wheel rotation and tyre burst behaviour dominate load path.

## Verify
- [ ] Intrusion at the specified measurement points within the structure criteria in CAE and test.
- [ ] Dummy kinematics keep head within the airbag coverage.
