---
id: engineering-technology.automotive-vehicle-engineering.crash-safety.neck-and-femur-injury-criteria
name: neck-and-femur-injury-criteria
category: engineering-technology
field: automotive-vehicle-engineering
product: crash-safety
tags: [neck-injury, nij, femur-load, tibia-index, injury-criteria, lower-extremity]
level: practitioner
status: gated
description: "Calculate Nij from neck loads and moments, check femur and tibia criteria, with critical values as in FMVSS 208 and how consumer tests treat them."
sources:
  - "FMVSS 208 injury criteria (nhtsa.gov); confirm current critical values"
  - "Kleinberger et al., Development of improved injury criteria for the assessment of advanced automotive restraint systems (NHTSA 1998)"
  - "https://www.law.cornell.edu/cfr/text/49/571.208"
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# Neck and femur injury criteria

1. **Nij:** combination of axial force and sagittal bending moment at the upper neck: `Nij = Fz/Fzc + My/Myc`. FMVSS 208 critical intercepts (S6.6, checked in 49 CFR 571.208; other dummies differ): tension 6806 N, compression 6160 N, flexion moment 310 N m, extension moment 135 N m; Nij must not exceed 1.0; peak tension is limited to 4170 N and peak compression to 4000 N.
2. Data: upper neck load cell Fz and My, filtered CFC 600; compute the four combinations (tension-flexion, tension-extension, compression-flexion, compression-extension) and report the maximum.
3. **Femur:** axial force limit in FMVSS 208 is 2250 lbf (about 10.0 kN) for the 50th male (S6.5) and 6805 N (1530 lbf) for the 5th female (S15.3.5); ECE R94 uses femur force vs time (a time-dependent limit) (gated: unconfirmed, source is paywalled or blocked); knee-thigh-hip loads depend on knee bolster and instrument panel design.
4. **Tibia:** tibia index combines force and bending moment (limit about 1.3 (gated: unconfirmed, source is paywalled or blocked)) and compressive force limit; used in ECE R94 and consumer ratings.
5. Design levers: knee bolster energy absorption, steering column design, pedal break-away, footwell intrusion, head restraint and airbag effects on the neck.
6. Cross-check the signals for crosstalk and zero drift.
7. Remember the dummy-specific scaling: values differ for the small female (5th) and other dummies.

**Gotchas:** wrong sign convention for flexion and extension moments.

## Verify
- [ ] Hand calculation of Nij from raw channels matches the post-processing software.
- [ ] Critical values and dummy type documented per test.
