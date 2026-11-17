---
id: architecture-construction.structural-trades.rigging-dogging.estimating-loads-selecting-slings-and-directing-crane-lifts
name: estimating-loads-selecting-slings-and-directing-crane-lifts
category: architecture-construction
field: structural-trades
product: rigging-dogging
tags: [structural-trades, rigging-dogging, rigging, dogging, dogman, rigger, slinging, crane-signals, hand-signals, load-estimation, centre-of-gravity, sling-angle, wll, working-load-limit, swl, chain-slings, wire-rope-slings, round-slings, webbing-slings, shackles, hooks, spreader-beam, tag-lines, choker-hitch, basket-hitch, exclusion-zone, lift-plan, critical-lift]
level: practitioner
status: draft
description: "Rig and direct a crane lift: estimate load weight and centre of gravity, pick slings by WLL and sling angle, inspect gear, signal the operator and run the exclusion zone."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Estimating loads, selecting slings and directing crane lifts

**Goal:** know what the load weighs and where its centre of gravity is, rig it with gear
rated above the actual sling loads (not just the load weight), and control the lift so
no one is ever under it. Dogging/rigging is a licensed or certified activity in many
places (e.g., high-risk work licence in AU, qualified rigger/signal person under OSHA
1926 Subpart CC in the US, CPCS/NPORS cards in the UK).

## 1. Know the weight
- Use the marked weight, delivery docket, or drawings. Otherwise calculate:
  volume × density. Steel ~7,850 kg/m³; reinforced concrete ~2,400–2,500 kg/m³;
  timber ~500–700 kg/m³ (wet heavier).
  e.g., precast slab 6 m × 2.4 m × 0.2 m = 2.88 m³ × 2,500 = 7,200 kg.
- Add rigging weight (spreader beams can be heavy). If unsure, assume heavier, and
  use a load cell where available.

## 2. Find the centre of gravity
- Symmetrical loads: in the middle. Irregular loads: estimate, then **test lift** a few
  centimetres — a tilting load tells you the CG isn't under the hook.
- Hook must be directly above the CG or the load swings/tilts on lift.

## 3. Sling angle and selection
- Sling tension rises as the angle between sling legs widens. Load per leg (2-leg,
  vertical-ish) ≈ load ÷ (number of legs × cos of the angle from vertical).
  - Included angle 60° (30° from vertical): each leg ≈ 0.58 × load.
  - Included angle 90°: each leg ≈ 0.71 × load.
  - Included angle 120°: each leg = **1.0 × load** — avoid beyond ~120° included.
- Many rating charts assume only **two legs share load** on a 4-leg sling for
  rigid loads (the others may go slack). Rate accordingly.
- **Hitch reduces capacity:** choker hitch roughly 75–80% of vertical WLL (less at sharp
  choke angles); basket hitch up to 2× (if legs vertical).
- Protect slings from sharp edges (corner packers/edge protectors) — sharp edges cut
  synthetic slings instantly and damage wire rope.

## 4. Inspect gear before use
- Tag/WLL legible; within inspection date.
- Chain: no stretched, nicked or twisted links; hooks with latches, no throat opening.
- Wire rope: broken wires, kinks, bird-caging, crushing, corrosion → remove.
- Synthetic: cuts, abrasion, heat/chemical damage, label missing → remove.
- Shackles: correct pin, fully screwed in (moused for long-term rigging), load on the bow
  in line.

## 5. Lift plan and exclusion zone
- Crane capacity at the radius with all rigging, ground conditions, overhead power lines
  (keep the prescribed clearances), wind limits.
- Critical lifts (near capacity, tandem, over occupied areas, personnel) need a formal
  written lift plan.
- Barricade the zone; nobody walks under a suspended load, ever.

## 6. Directing the lift
- One person signals — agreed hand signals (national standard set) or radio with a
  dedicated channel and continuous talk-through.
- Test lift ~100–300 mm, hold: check balance, slings seated, brakes holding.
- Tag lines to control rotation (never wrap around a hand or body).
- Land on dunnage so slings can be removed without crushing; ensure the load is stable
  before slacking off and unhooking.
- **Stop** for wind over the crane's limit, lost communication, or anything unexpected.

## Gotchas
- Rating the sling for the load instead of the leg tension at the actual angle.
- Synthetic slings over unprotected steel edges.
- Assuming all four legs share load.
- Hands near pinch points during landing.

## Verify
- [ ] Load weight known (calc or marked) and CG under hook (test lift level).
- [ ] Sling leg tension at the actual angle ≤ WLL with hitch reduction applied.
- [ ] All gear tagged, inspected and free of defects.
- [ ] Exclusion zone set; one signaller; communication tested.
- [ ] Load landed stable on dunnage before unhooking.

*Status: draft — angle factors are trigonometry; capacity tables, signals and licensing
are jurisdiction- and manufacturer-specific.*
