---
id: engineering-technology.civil-engineering.transportation-highway-design.stopping-sight-distance
name: stopping-sight-distance
category: engineering-technology
field: civil-engineering
product: transportation-highway-design
tags: [sight-distance, stopping-sight-distance, ssd, perception-reaction-time, crest-vertical-curve, sag-curve, decision-sight-distance, aashto-green-book, design-speed]
level: practitioner
status: draft
description: "Check stopping sight distance on horizontal and vertical alignment: SSD formula, reaction time, deceleration, crest/sag curve lengths, grade and obstruction offset."
sources: ["AASHTO A Policy on Geometric Design of Highways and Streets (Green Book), current edition", "Austroads Guide to Road Design Part 3", "Garber and Hoel, Traffic and Highway Engineering"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Stopping sight distance (SSD)

AASHTO SI: SSD = 0.278 V t + V^2 / (254 (a/9.81 + G)), V in km/h, brake reaction t = 2.5 s, a = 3.4 m/s2 (comfortable deceleration), G grade as decimal (+ uphill). US: SSD = 1.47 V t + V^2 / (30 (a/32.2 + G)), a = 11.2 ft/s2.

## Checks
1. Use design speed (not posted speed); downgrades need more distance.
2. Crest vertical curve: driver eye 1.08 m, object 0.6 m (current Green Book; confirm the adopted edition). With S < L: L = A S^2 / (200 (sqrt(h1) + sqrt(h2))^2), A algebraic grade difference in percent, heights in m. K = L/A.
3. Sag curve (headlight control): headlight height 0.6 m, 1 degree upward divergence: L = A S^2 / (120 + 3.5 S) for S < L.
4. Horizontal curve: lateral clearance to cut face, wall or barrier m = R (1 - cos(28.65 S / R)) (S, R in metres; the angle is in degrees).
5. Intersections need intersection sight distance (longer) separately.

## Gotchas
- Authorities differ (AASHTO, Austroads, UK DMRB) in reaction time, heights and deceleration. State which you applied.
- Truck eye height helps on crests; hurts under overbridges on sags.

## Verify
Check the sight line in the profile view (e.g. a Civil 3D sight-distance analysis) at every station.

> Professional guidance only. Design, sign-off and site decisions belong to a licensed/chartered engineer applying the codes adopted in the project jurisdiction; check edition and local amendments.
