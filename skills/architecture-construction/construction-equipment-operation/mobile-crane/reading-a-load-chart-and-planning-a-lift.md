---
id: architecture-construction.construction-equipment-operation.mobile-crane.reading-a-load-chart-and-planning-a-lift
name: reading-a-load-chart-and-planning-a-lift
category: architecture-construction
field: construction-equipment-operation
product: mobile-crane
tags: [construction-equipment-operation, mobile-crane, all-terrain-crane, rough-terrain-crane, truck-crane, crawler-crane, load-chart, rated-capacity, lift-plan, lift-study, radius, boom-length, outriggers, outrigger-pads, mats, ground-bearing-pressure, rigging-weight, deductions, critical-lift, appointed-person, lifting-supervisor, asme-b30-5, bs-7121, as-2550, lmi, rated-capacity-limiter]
level: advanced
status: draft
description: "Planning a mobile crane lift from the load chart: gross load, radius, boom length, outrigger setup, deductions, ground bearing pressure, and percentage-of-capacity limits."
sources: ["ASME B30.5 Mobile and Locomotive Cranes", "BS 7121 Code of practice for safe use of cranes", "AS 2550 Cranes, hoists and winches - Safe use", "OSHA 29 CFR 1926 Subpart CC (Cranes and Derricks in Construction)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reading a load chart and planning a lift

**Goal:** confirm, before the crane is rigged, that the gross load is within the
manufacturer's rated capacity at the worst radius of the lift, for the exact
configuration you will use, on ground that can carry the outrigger loads.

Lifts are planned by a competent/appointed person under your jurisdiction's rules
(ASME B30.5 / OSHA Subpart CC, BS 7121, AS 2550 and so on). The **manufacturer's load
chart for that serial-numbered crane is the only authority**; numbers here are examples.

## 1. Establish the gross load
Gross load = everything hanging below the boom tip that the chart does not already
include. Typically:
- load weight (from the delivery note, drawing or a weighed figure — not a guess);
- rigging: slings, shackles, spreader beam, tag lines;
- hook block or headache ball;
- hoist rope below the sheaves on some charts;
- stowed or erected jib/fly, and any deductions the chart notes say apply.
Read the chart's notes page: what is and is not deducted differs by manufacturer.

## 2. Find the worst radius
Radius is measured horizontally from the centre of rotation to the hook (load centre),
**not** from the outrigger or the cab. Measure on the drawing or site:
- pick-up point, set-down point, and any point in between where the slew takes the load
  further out;
- add allowance for boom deflection, which increases radius under load (several
  hundred millimetres on long booms).
Plan on the largest radius in the whole movement.

## 3. Read the correct chart
Select the table that matches **all** of: counterweight fitted, outrigger extension
(full, mid, retracted), working area (over rear, over side, 360°), boom length and
jib configuration. Then:
1. Find the boom length column that will reach (check the range/height diagram that
   the boom clears the structure).
2. Read capacity at the next **larger** radius listed — never interpolate upward. If
   your radius is 13.2 m and rows are 12 m and 14 m, use 14 m.
3. Bold or shaded values are often structural limits; others are stability limits —
   the notes explain which, and it matters for how the crane fails.

## 4. Apply your margin
Utilisation = gross load ÷ chart capacity. Common practice treats over about 75–85%
as a planned/critical lift needing a written plan and extra checks, and many
companies cap ordinary lifts there (unverified — thresholds vary by company and
regulator; some use 90%). Wind, side loading and dynamic effects are not in the
chart margin beyond what the manufacturer states.

## 5. Ground and outriggers
- Maximum outrigger load can be a large share of crane plus load weight — use the
  manufacturer's outrigger load calculator or app where available.
- Ground bearing pressure = outrigger load ÷ mat area. Compare with the allowable
  bearing capacity from a site assessment or geotech; typical figures for compacted
  ground are in the low hundreds of kPa, soft clay far less (unverified — get the
  actual value).
- Size mats/timbers so the pressure is within capacity; check for voids, trenches,
  basements and services under each outrigger.
- Level the crane within the manufacturer's tolerance (often around 1%).

## 6. Write it down
Lift plan: load and gross weight, configuration, worst radius, chart capacity,
utilisation, ground pressure, rigging spec, exclusion zone, signaller, wind limit and
communication method. Brief the crew before the lift.

## Gotchas
- Setting the RCI/LMI to the wrong configuration makes it lie; check its mode matches
  the real setup before every lift.
- A load "on the chart" over the front can be off the chart over the side.
- Lifting from water, out of mud or with suction adds weight the scales never saw.
- Hook-block weight on big cranes can be over a tonne — easy to forget.
- Wind on large-area loads (panels, roof trusses) can exceed the crane's in-service
  limit well below the published maximum wind speed.

## Verify
- [ ] Gross load includes rigging, hook block and chart-note deductions.
- [ ] Worst radius identified across the whole slew, with deflection allowance.
- [ ] Chart matches counterweight, outriggers, work area and boom/jib configuration.
- [ ] Capacity read at the next larger radius; utilisation within your company limit.
- [ ] Ground pressure under each mat checked against a known bearing capacity.
- [ ] LMI set to the actual configuration; plan briefed and signed.
