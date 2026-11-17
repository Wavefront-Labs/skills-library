---
id: architecture-construction.structural-trades.steel-fixing.reading-bar-schedules-and-fixing-reinforcement-to-cover
name: reading-bar-schedules-and-fixing-reinforcement-to-cover
category: architecture-construction
field: structural-trades
product: steel-fixing
tags: [structural-trades, steel-fixing, steel-fixer, rebar, reinforcement, reinforcing-steel, bar-schedule, bending-schedule, bar-marks, shape-codes, bs-8666, as-1100-501, laps, lap-splices, development-length, cover, concrete-cover, chairs, spacers, bar-chairs, tie-wire, tying-patterns, saddle-tie, mesh, fabric, couplers, starter-bars, cover-meter, pre-pour-inspection]
level: practitioner
status: draft
description: "Fix reinforcement from bar schedules and drawings: decode bar marks and shape codes, place to spacing, laps and cover with chairs and spacers, tie securely, pass inspection."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reading bar schedules and fixing reinforcement to cover

**Goal:** every bar of the right size, shape and position, at the specified spacing, lap
and cover, tied firmly enough to stay put through the pour.

## 1. Reading the drawings and schedule
- **Bar mark notation** (UK style example): `12 H16-03-200 B1` = 12 bars, high-yield
  16 mm diameter, bar mark 03, at 200 mm centres, bottom outer layer. US style uses bar
  sizes (#5 = 5/8 in) and "@ 8 in o.c."; AU uses N16, etc. Learn the convention on the
  drawing legend.
- Layers: B1/B2 (bottom outer/inner), T1/T2 (top outer/inner) — orientation matters for
  cover and effective depth.
- **Bar schedule** gives each mark's shape code (BS 8666 / AS 1100.501 / ACI shapes),
  dimensions, number and length. Check delivered bundles' tags against it.

## 2. Cover — the most important number
- **Cover** = distance from the concrete surface to the *nearest* steel, including
  links/stirrups. Specified per element and exposure (e.g., 25–40 mm internal,
  50–75 mm in ground or severe exposure — **from the drawings, not from memory**).
- Too little cover → corrosion and spalling, reduced fire resistance. Too much → reduced
  structural depth and cracking.
- Achieve with **spacers/chairs** of the right height: plastic or concrete spacers under
  bottom bars (concrete ones in exposed faces where plastic is not allowed), chairs to
  hold top mats. Spacing of supports per spec (often ~0.75–1 m) so bars don't sag between.

## 3. Spacing and placing
- Mark bar positions on the formwork or on a chalked bar with a tape — don't eyeball
  200 mm centres across a large slab.
- First bar at about half a spacing (or the drawing's edge distance) from the edge.
- Bend radii, hook orientation and anchorage lengths as scheduled; hooks turned so
  they're inside the cover zone.
- Around openings: trimmer bars as detailed.

## 4. Laps and couplers
- **Lap length** per drawing (often expressed as a multiple of bar diameter, e.g.,
  40–60 × d depending on concrete, bar position and code). Stagger laps where the
  drawings require; don't lap all bars at one section unless allowed.
- Mechanical couplers: approved type, threads clean and fully engaged per manufacturer
  (often with a witness mark).
- Starter bars: check projection length and position before the first pour — wrong
  starters are expensive to fix (drilling and chemical anchoring needs engineer approval).

## 5. Tying
- Tie at intersections per spec: slabs often every other intersection in the field and
  every intersection at edges/laps; walls and beams more. Use the tie that resists the
  expected movement (snap tie, saddle tie, figure-eight).
- Turn tie wire ends inward, away from the cover zone (wire tails in cover rust and stain).
- The cage must take foot traffic during the pour — walk boards on mats.

## 6. Before the pour
- Clean: no mud, oil or release agent on bars; loose rust is OK, flaking rust isn't.
- Cast-ins (ducts, anchors, conduits) fixed without displacing bars; no bars cut for
  services without engineer approval.
- Inspection hold point: engineer/inspector checks size, spacing, laps, cover.

## Gotchas
- Spacers sized for the bar instead of the cover required.
- Top mat chairs too far apart → mat crushed under foot.
- Cutting bars to fit plumbing sleeves.
- Laps shortened to suit delivered lengths.

## Verify
- [ ] Every bar mark placed matches the schedule (count, size, shape).
- [ ] Cover checked with a tape at multiple points (and cover meter after pour if specified).
- [ ] Spacing measured across each mat; laps and starters measured.
- [ ] Cage rigid under foot; tie tails turned in.
- [ ] Pre-pour inspection signed.

*Status: draft — notation examples from BS 8666/AS conventions; cover and lap values are
project-specific.*
