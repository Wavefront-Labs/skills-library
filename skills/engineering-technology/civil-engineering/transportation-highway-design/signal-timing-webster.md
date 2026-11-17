---
id: engineering-technology.civil-engineering.transportation-highway-design.signal-timing-webster
name: signal-timing-webster
category: engineering-technology
field: civil-engineering
product: transportation-highway-design
tags: [signal-timing, webster, cycle-length, lost-time, critical-lane-volumes, flow-ratio, green-split, yellow-change, all-red, intersection-capacity]
level: practitioner
status: draft
description: "Set a fixed-time signal plan with Webster's method: lost time, critical flow ratios, optimum cycle, green splits, yellow and all-red, and checks afterwards."
sources: ["Webster, Traffic Signal Settings (Road Research Technical Paper 39, 1958)", "ITE/FHWA Traffic Signal Timing Manual", "Highway Capacity Manual (TRB), signalised intersections", "Garber and Hoel, Traffic and Highway Engineering"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Fixed-time signal plan (Webster)

## Inputs
Phase structure, design-hour volumes per lane group, saturation flow rates (HCM default about 1900 pc/h/lane; measure if possible).

## Computation
1. Flow ratio y = v/s per lane group; critical y per phase is the largest among movements served; Y = sum of critical y.
2. Lost time per phase L = startup lost time + clearance lost time (yellow + all-red minus the part used by drivers); total lost time = sum.
3. Webster optimum cycle: C0 = (1.5 L + 5)/(1 - Y) s. If Y exceeds about 0.85 to 0.9 the junction is near capacity and the formula is not valid: add lanes or change phasing. Practical cycles are usually 60 to 120 s.
4. Effective green total = C - L, split in proportion to critical y: g_i = (C - L) y_i / Y.
5. Yellow change (ITE): y = t + v/(2a + 2Gg), t about 1 s, a about 3 m/s2. All-red = (W + L_vehicle)/v. Pedestrian times from crossing distance and walking speed per the manual in force (MUTCD edition or local equivalent).

## Check
Evaluate delay and level of service (HCM, Synchro or similar) and queue storage; revise if v/c exceeds 1 on any group. Webster minimises delay for random arrivals and ignores coordination.

## Verify
Greens + lost time = cycle; each phase meets minimum green and pedestrian time.

> Professional guidance only. Design, sign-off and site decisions belong to a licensed/chartered engineer applying the codes adopted in the project jurisdiction; check edition and local amendments.
