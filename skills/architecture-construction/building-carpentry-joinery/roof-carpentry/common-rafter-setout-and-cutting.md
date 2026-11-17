---
id: architecture-construction.building-carpentry-joinery.roof-carpentry.common-rafter-setout-and-cutting
name: common-rafter-setout-and-cutting
category: architecture-construction
field: building-carpentry-joinery
product: roof-carpentry
tags: [roof-carpentry, roof-framing, cut-roof, rafters, common-rafter, pitch, roof-pitch, rise-and-run, span, half-span, rafter-length, plumb-cut, seat-cut, birdsmouth, ridge-board, ridge-beam, wall-plate, top-plate, overhang, eaves, fascia, soffit, framing-square, speed-square, rafter-tables, pattern-rafter, collar-tie, ceiling-joists, hip-and-valley, pythagoras]
level: practitioner
status: draft
description: "Set out and cut common rafters for a gable roof: span, pitch and true length by calculation, plumb and seat cuts, birdsmouth limits, ridge deduction and overhang, then a tested pattern rafter."
sources: ["General roof-framing trade practice (framing square and rafter tables)", "TRADA / NHBC guidance on cut roofs (UK)", "IRC R802 roof framing (US)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Common rafter setout and cutting

**Goal:** a set of identical common rafters that sit tight on the wall plate and ridge,
giving a straight ridge and an even eaves line — calculated, proven with one pattern,
then copied.

> Rafter size, spacing, birdsmouth depth and ties are **structural**: take them from the
> engineer's design or span tables for your code. This skill covers geometry and cutting.

## 1. Gather the numbers
- **Span**: outside of wall plate to outside of wall plate, measured at several points
  (walls are rarely parallel — note the variation).
- **Run** = half the span (for an equal-pitch gable).
- **Pitch**: in degrees, or rise per unit run (e.g. 6/12 ≈ 26.57°).
- Ridge board thickness; overhang (horizontal) to fascia line.

## 2. Calculate the rafter length (theoretical line)
- `rise = run × tan(pitch)`.
- `line length = √(run² + rise²) = run ÷ cos(pitch)`.
- **Ridge deduction:** shorten by half the ridge thickness *measured horizontally*,
  i.e. `(ridge ÷ 2) ÷ cos(pitch)` along the slope.
- **Overhang** along the slope = `horizontal overhang ÷ cos(pitch)`.
Example: span 7,200 mm → run 3,600; pitch 35°; ridge 38 mm.
Line length = 3,600 ÷ cos35° = 4,395 mm. Ridge deduction = 19 ÷ 0.819 = 23 mm →
4,372 mm from ridge plumb cut to the plate's outer line. Overhang 450 mm horizontal →
549 mm on slope.
(Framing-square rafter tables or a construction calculator give the same; the maths
lets you check them.)

## 3. Mark the pattern rafter
Measure lengths along a consistent **measuring line**, usually the line from the outer
top edge of the wall plate (the "height above plate" line).
1. **Plumb cut at the ridge:** set a speed square or framing square to the pitch and
   mark a vertical line.
2. Measure the shortened line length down the rafter to the plate line; mark a second
   plumb line (the birdsmouth's vertical face).
3. **Seat cut** (horizontal) of the birdsmouth: square off the plumb line. Typical limit:
   seat depth no more than about **⅓ of rafter depth** so enough timber remains above
   the plate (follow the design). Make the "height above plate" (HAP) identical on every
   rafter — this is what keeps the ridge straight.
4. Add the overhang beyond the plumb line and mark the tail plumb cut (and level soffit
   cut if the soffit is horizontal).

## 4. Prove the pattern
Cut the pattern and a second rafter; offer them up as a pair at both gable ends with a
ridge offcut between. Check: plumb cuts meet fully, seats bear fully on the plate,
ridge height matches the calculated `rise + HAP`. Adjust the pattern, not each rafter.

## 5. Production
- Crown every rafter upward; mark the crown before laying out.
- Trace the pattern onto stock and cut all. Cut birdsmouths carefully — overcutting the
  inside corner weakens the rafter; finish corners with a handsaw.
- Install: gable rafters and ridge first, propped plumb and braced; check ridge straight
  and level with a string line; then fill in at layout centres (e.g. 400 / 600 mm or
  16/24") marked on plate and ridge together.
- Fix to plates with skew nails/screws or straps/hurricane ties as designed; collar ties
  or ceiling joists tie rafter feet against spread.

## Gotchas
- Walls out of parallel: varying span means varying rafter seats; keep the HAP constant
  and accept the overhang varying slightly, or pack the plate.
- Mixing up the measuring line (top edge vs centreline) shifts all lengths.
- Hips and valleys need their own backing/bevel calculations — separate skill.

## Verify
- [ ] Span measured at several points; run and rise calculated.
- [ ] Ridge deduction applied horizontally and converted to slope.
- [ ] Pattern pair proven in place before production cutting.
- [ ] HAP identical on every rafter; ridge string-line straight and level.
- [ ] Ties/straps installed per the structural design.
