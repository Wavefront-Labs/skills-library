---
id: architecture-construction.electrical-installation.conduit-cable-containment.conduit-bending-and-cable-pulling
name: conduit-bending-and-cable-pulling
category: architecture-construction
field: electrical-installation
product: conduit-cable-containment
tags: [electrical-installation, conduit-cable-containment, conduit, emt, rigid-conduit, imc, pvc-conduit, hand-bender, conduit-bending, offset-bend, saddle-bend, back-to-back, take-up, shrink, conduit-fill, space-factor, trunking, raceway, fish-tape, pulling-lubricant, cable-pulling, jam-ratio, segregation, nec-chapter-9, bs-7671]
level: practitioner
status: draft
description: "Bend EMT/steel/PVC conduit (90s, offsets, saddles) with take-up and shrink figures, respect fill and bend limits, then pull cables safely with lube and a fish tape."
sources: ["NFPA 70 National Electrical Code (NEC) Chapter 9 and Articles 344, 352, 358", "BS 7671 Requirements for Electrical Installations", "AS/NZS 3000 Wiring Rules"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Conduit bending and cable pulling

**Goal:** produce a conduit run (US "raceway") that lands exactly where marked, stays
within fill and bend limits, and lets cables pull in without damaging insulation.

> **Licensed, jurisdiction-specific work.** Containment is part of the fixed wiring
> system; rules on fill, supports and segregation differ by jurisdiction. The bending
> figures below are typical for common US hand benders; your bender's markings and your
> edition of the wiring rules win.

## 1. Plan the run
- **Bends between pull points:** US NEC limits a run to 360° total (e.g. four 90s)
  between boxes/fittings; fewer bends make pulling far easier. UK/AU practice uses draw-in
  boxes at intervals set by run length and bends (unverified — confirm against your
  edition of the wiring rules).
- **Fill:** US NEC Chapter 9: 53% of the internal area for one conductor, 31% for two, 40%
  for three or more. UK: cable factor/space-factor tables, trunking typically ≤45%
  space factor.
- **Segregation:** keep LV power apart from data/ELV/fire-alarm (separate conduit or
  divided trunking, or cables insulated for the highest voltage present).
- **Supports:** at the spacing the rules require (US EMT: within 3 ft (900 mm) of each box
  and every 10 ft (3 m)).

## 2. Hand-bending EMT: the key numbers
Mark from the conduit end; the bender's arrow, star and rim marks are references.
- **Stub-up 90°:** mark = desired stub height − **take-up**. Typical take-up:
  1/2 in EMT 5 in, 3/4 in 6 in, 1 in 8 in (check the bender).
- **Back-to-back 90°:** measure to the *back* of the first 90 and align with the star mark.
- **Offsets** (two equal opposite bends) — distance between marks = offset depth ×
  multiplier; shrink is lost run length per inch of offset depth:

  | angle | multiplier | shrink per inch of depth |
  |---|---|---|
  | 10° | 6.0 | 1/16 in |
  | 22.5° | 2.6 | 3/16 in |
  | 30° | 2.0 | 1/4 in |
  | 45° | 1.4 | 3/8 in |
  | 60° | 1.2 | 1/2 in |

  Example: 4 in offset at 30° → marks 8 in apart; add 1 in for shrink when the offset
  must land at a fixed obstruction distance.
- **3-point saddle** (over a pipe): centre bend 45°, two outer bends 22.5°; outer marks
  ≈2.5 × obstruction height from the centre mark; shrink ≈3/16 in per inch of height.
- Keep all bends in one plane (check with a level on the conduit) — "dog-legs" won't sit flat.

## 3. Cutting and joining
Cut square, **ream every cut end** (sharp burrs strip insulation), fit couplings and
connectors tight — steel conduit may be the protective conductor. PVC: solvent cement,
heat-bend with a bending spring or heater box, and fit **expansion joints** on long
outdoor runs.

## 4. Pulling cables
1. **Isolate** any circuits already in the containment if you will disturb them: lock
   off, tag, prove the tester, test dead, re-prove. New cables must not be terminated
   at a live board.
2. Run a fish tape (or vacuum a "mouse" with draw string through long runs); pull in a
   rope rated for the job.
3. Stagger and tape the conductor ends into a smooth head; on big pulls use a basket grip.
4. Apply **pulling lubricant** compatible with the cable sheath; feed from the end
   nearest the most bends where possible so tension rises less.
5. One person feeds (keeping cables straight, no crossovers), one pulls steadily.
   Don't exceed the cable maker's maximum pulling tension or bending radius.
6. **Jam ratio:** three cables can wedge when conduit ID ÷ cable OD is about 2.8–3.2;
   change conduit size if you're in that band (unverified — confirm against the cable
   maker's pulling guide).
7. Leave tails long enough to terminate; label both ends.

## Gotchas
- Too many bends between pull points is the #1 cause of stripped cables.
- Pulling on conductors around a sharp, unreamed edge slices insulation invisibly — IR
  testing finds it later.
- Kinked conduit (bender slipped) reduces area; cut it out.
- Mixing power and data in the same unsegregated containment fails inspection and induces noise.

## Verify
- [ ] Bends ≤ the limit between pull points; all bends in plane, no kinks.
- [ ] Fill/space factor within limits; segregation maintained.
- [ ] Every cut end reamed; couplings tight; supports at required spacing.
- [ ] Existing circuits isolated and proved dead before disturbing them.
- [ ] Cables undamaged after pulling — confirmed by insulation-resistance test.
