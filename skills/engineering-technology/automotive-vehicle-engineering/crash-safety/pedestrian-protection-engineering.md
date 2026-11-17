---
id: engineering-technology.automotive-vehicle-engineering.crash-safety.pedestrian-protection-engineering
name: pedestrian-protection-engineering
category: engineering-technology
field: automotive-vehicle-engineering
product: crash-safety
tags: [pedestrian-protection, un-r127, gtr-9, headform-impact, legform, active-bonnet, vulnerable-road-user]
level: practitioner
status: gated
description: "Engineer pedestrian protection: headform and legform tests, bonnet and bumper design, clearance to hard points, active bonnets and AEB interplay."
sources:
  - "UN Regulation 127 and UN GTR 9; Euro NCAP vulnerable road user protocols; confirm current versions"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Pedestrian protection

0. All test speeds and HIC limits below are unconfirmed (gated: unconfirmed, source is paywalled or blocked).
1. Tests: child and adult headform impactors fired at the bonnet top and windscreen base at about 35 km/h; upper legform and flexible lower legform (FlexPLI) at the bumper at about 40 km/h. UN GTR 9 / UN R127 set limits (for example head injury criterion limits split into zones, around 1000 and 1700; confirm the text).
2. Design head impact zones: provide deformation space (often 50-100 mm or more of clearance between the bonnet skin and hard parts such as engine, strut tops, hinges), with deformable hinges and energy-absorbing structure; map the wrap-around distance zones.
3. Bumper and legs: soft bumper foam or absorber, lower stiffener bar to control tibia/knee loads; bumper lead.
4. Windscreen base and A-pillar: the head impact area has specific provisions; many are excluded from compliance but included in consumer tests.
5. Active systems: pop-up bonnet raises the rear of the bonnet on pedestrian detection to open clearance; pedestrian airbag; both need reliable sensing.
6. AEB: autonomous emergency braking for pedestrians and cyclists is assessed in consumer programmes and in some regulations; coordinate with vehicle safety systems.
7. CAE with headform and legform models, then physical testing of concept areas.

**Gotchas:** tradeoff with styling (high bonnet, low clearance) and with engine package.

## Verify
- [ ] Head impact grid points mapped; HIC predictions below limits with margin.
- [ ] Legform results within criteria in CAE and prototype test.
