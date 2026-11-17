---
id: architecture-construction.building-carpentry-joinery.staircase-construction.stair-setout-and-stringer-cutting
name: stair-setout-and-stringer-cutting
category: architecture-construction
field: building-carpentry-joinery
product: staircase-construction
tags: [staircase-construction, stairs, stair-building, stair-setout, rise-and-going, rise-and-run, total-rise, riser-height, going, tread-depth, 2r-plus-g, blondel-formula, stringer, string, cut-string, closed-string, housed-stringer, framing-square, stair-gauges, pitch, headroom, nosing, first-step, last-step, building-regulations-part-k, irc-r311, handrail-height, balustrade, 100mm-sphere, winders]
level: practitioner
status: draft
description: "Set out and cut a straight stair: total rise to finished floors, equal risers and goings within code, 2R+G, pitch and headroom checks, stringer marking and the bottom-step drop."
sources: ["UK Approved Document K (Protection from falling, collision and impact)", "US IRC R311.7 stairways", "General stair-building trade practice"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Stair setout and stringer cutting

**Goal:** a straight flight where **every riser is identical** (people trip on a step
even ~5–10 mm different), within the building code, with headroom, using stringers cut
right first time.

> Code values below are typical examples (UK Part K / US IRC); verify the edition and any
> local amendment before cutting. Private dwelling and public stair limits differ.

## 1. Measure total rise — to *finished* floors
Measure floor-to-floor at the stair position, then adjust for floor finishes not yet
laid: `total rise = structural rise − bottom finish thickness + top finish thickness`.
Ignoring a 20 mm tile + screed at the bottom is the classic error: the first step ends up
short or tall.

## 2. Calculate risers and goings
1. Divide total rise by a target riser (~180–190 mm or ~7–7¾") and round **up** to whole
   risers: `n = ceil(total rise ÷ target)`.
2. `riser = total rise ÷ n` (keep the decimals; mark accurately).
3. Number of treads (goings) on a stair that lands on the upper floor = **n − 1**.
4. Choose a going and check limits:
   - UK private stair: rise 150–220 mm, going 220–300 mm, **2R + G = 550–700 mm**,
     pitch ≤ 42°.
   - US IRC: riser ≤ 7¾" (196 mm), tread ≥ 10" (254 mm) plus nosing rules.
   - A comfortable 2R+G is often around 600–630 mm.
5. Total going = going × (n − 1). Check it fits the stairwell length and the landing
   space at top and bottom.
Example: rise 2,640 mm → 2,640 ÷ 190 = 13.9 → 14 risers of 188.6 mm; 13 goings of 245 mm
→ 2R+G = 622 ✓; total going 3,185 mm; pitch = atan(188.6/245) ≈ 37.6° ✓.

## 3. Headroom
Draw the pitch line in section and check clearance vertically above it to the trimmer/
ceiling: e.g. UK ≥ 2.0 m (relaxations for loft conversions), US IRC ≥ 6'8" (2,032 mm).
If short, the stairwell opening must lengthen — sort this before cutting.

## 4. Mark the stringer (cut/open stringer)
- Stock: e.g. 2×12 / 300×50 or as engineered; check the remaining throat (material below
  the notch) — commonly ≥ ~3½"/90 mm (IRC-style rule; *check design*).
- Clamp **stair gauges** (or a fence) onto a framing square at the riser on the tongue
  and going on the blade.
- Step off from the top, marking each riser/tread triangle; check that the final tally
  matches n.
- **Drop the bottom**: cut the bottom of the stringer short by **one tread thickness**
  (minus the bottom finish if that is already in) — otherwise the first step is taller
  than the rest by the tread thickness. Similarly the top riser is reduced if treads sit
  on top of the stringer.
- Cut with a circular saw, stopping short of the inside corner; finish with a hand saw or
  jigsaw — overcutting weakens the stringer.
- Use the first stringer as a template; check it in place before cutting others.

## 5. Housed (closed) strings
For joinery stairs, treads and risers sit in tapered housings routed into the strings
with a template jig and are glued and wedged from below; glue blocks under each
tread-riser junction stop creaks. Usually shop-made — measure accurately and supply total
rise and going to the stair maker.

## 6. Balustrade and handrail
Typical: handrail height 900–1,000 mm above pitch line (UK), 34–38" (US); openings must
not pass a **100 mm sphere** (UK) / 4" sphere (US). Handrail on at least one side,
both if wide.

## Gotchas
- Winders and mixed flights need full-size setout; rules on minimum going at the
  narrow end apply — *specialist check.*
- Changing finish plans late (adding carpet pads, thick tiles) breaks equal risers.

## Verify
- [ ] Total rise measured to finished floor levels.
- [ ] All risers equal within ~2–3 mm; 2R+G and pitch within code.
- [ ] Headroom clear along the full pitch line.
- [ ] Bottom of stringer dropped by tread thickness; first step measured.
- [ ] Balustrade passes the sphere test; handrail height checked.
