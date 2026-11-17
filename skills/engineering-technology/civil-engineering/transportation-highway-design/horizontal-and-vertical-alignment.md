---
id: engineering-technology.civil-engineering.transportation-highway-design.horizontal-and-vertical-alignment
name: horizontal-and-vertical-alignment
category: engineering-technology
field: civil-engineering
product: transportation-highway-design
tags: [transportation-highway-design, geometric-design, road-design, highway-design, horizontal-alignment, vertical-alignment, design-speed, superelevation, side-friction, minimum-radius, spiral, clothoid, transition-curve, superelevation-runoff, vertical-curve, k-value, crest-curve, sag-curve, stopping-sight-distance, ssd, headlight-sight-distance, aashto, green-book, austroads, gtrd-part-3, dmrb, alignment-coordination]
level: practitioner
status: verified
description: "Design road horizontal and vertical alignment: design speed, curve radius and superelevation, transitions, K values for crest and sag, stopping sight distance (AASHTO/Austroads)."
sources: ["AASHTO A Policy on Geometric Design of Highways and Streets (Green Book), 7th ed.", "Austroads Guide to Road Design Part 3: Geometric Design", "UK DMRB CD 109 Highway link design (Revision 1, March 2020, replaced TD 9/93 and TD 70/08; standardsforhighways.co.uk)", "Garber & Hoel, Traffic and Highway Engineering"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Horizontal and vertical alignment — consistent speed, adequate sight, comfortable curves

**Goal:** an alignment where every curve suits the speed drivers will actually travel,
every crest and curve leaves stopping sight distance, and plan and profile work
together. Numbers below are AASHTO Green Book (US) unless labelled; Austroads (AU/NZ)
and DMRB (UK) use the same physics with different parameters and tables — always design
to the one your authority adopts.

## 1. Design speed and the operating speed
- Choose design speed from road class, terrain and context (AASHTO), or — in
  Austroads — check **operating speed** using the speed-environment / operating-speed
  model so curves don't sit below what drivers will do on the approach.
- Aim for **consistency**: avoid one sharp curve after long fast tangents. A drop of
  more than about 10 km/h (≈ 5–10 mph) in curve speed relative to the approach is a
  common red flag (gated: unconfirmed, source is paywalled or blocked); Austroads gives explicit guidance.

## 2. Horizontal curves
Point-mass relation:
- SI: R_min = V² / [127·(e + f)]  (V km/h, R m)
- US: R_min = V² / [15·(e + f)]  (V mph, R ft)
where e = superelevation (decimal), f = side-friction factor.
- **e_max:** AASHTO tables for 4, 6, 8, 10, 12% (gated: unconfirmed, source is paywalled or blocked). Typical: 8% rural, 4–6% urban,
  ≤ 6% (or less) where snow/ice is common (gated: unconfirmed, source is paywalled or blocked).
- **f:** AASHTO design values decrease with speed (about 0.12 at 100 km/h and 0.08 at 130 km/h, with much larger values at low speeds, so do not use one f for all speeds; read the table (gated: unconfirmed, source is paywalled or blocked)). Austroads uses its own desirable/absolute f tables, also
  speed-dependent.
- Example (AASHTO, SI): V = 100 km/h, e = 8%, f ≈ 0.12 → R ≈ 100² / (127 × 0.20) ≈ 394 m (computed: 393.7 m; 127 = 9.81 × 3.6², US constant 15 checks to 14.97).
  The Green Book table rounds this; use the table value.
- For radii above the minimum, distribute e by the AASHTO Method 5 curves (or
  Austroads tables) rather than using e_max everywhere.

## 3. Transitions and superelevation development
- **Spirals (clothoids)** ease curvature change; AASHTO treats them as optional with
  guidance, Austroads and DMRB use them routinely on higher-speed roads.
- **Superelevation runoff** length from the maximum relative gradient between edge and
  centreline (AASHTO table, ~0.35–0.80% depending on speed (gated: unconfirmed, source is paywalled or blocked); Austroads similar).
- Without spirals: put about 60–80% of runoff on the tangent (AASHTO; 2/3 is the usual
  pick) (gated: unconfirmed, source is paywalled or blocked). With spirals: develop it over the spiral.
- Watch the flat spot where cross-fall passes through 0%: keep longitudinal grade
  ≥ ~0.5% there (or design for drainage) to avoid ponding and aquaplaning.

## 4. Stopping sight distance (SSD)
AASHTO: SSD = 0.278·V·t + 0.039·V²/a (SI), with t = 2.5 s and a = 3.4 m/s².
The formula gives (computed) 63 m at 50 km/h, 129 m at 80, 184 m at 100 and 249 m at 120; the Green Book's rounded table values (≈ 65, 130, 185, 250 m) are consistent (gated: unconfirmed, source is paywalled or blocked). Use the table.
Austroads uses its own reaction times and coefficient of deceleration; check Part 3 for current values (the 2.0–2.5 s range is unconfirmed (gated: source is paywalled or blocked)). Check SSD also on
horizontal curves against roadside obstructions (middle-ordinate / sight-line offset).

## 5. Vertical curves
Use the **K value** (length per 1% of algebraic grade change: L = K·A).
- **Crest (AASHTO, S < L):** L = A·S² / 658 (SI, eye 1.08 m, object 0.60 m (gated: unconfirmed, source is paywalled or blocked)). K = S²/658 at the SSD above gives (computed) 52 at 100 km/h and 26 at 80 km/h.
- **Sag (AASHTO, headlight control, S < L):** L = A·S² / (120 + 3.5·S) (gated: unconfirmed, source is paywalled or blocked). K = S²/(120+3.5S) gives (computed) 45 at 100 km/h and 29 at 80 km/h (Green Book tabulates 30). Comfort-based sag K can be used where lighting is
  continuous.
- Austroads uses different eye/object heights (eye ~1.1 m for cars) and publishes its
  own K tables; DMRB tabulates "desirable minimum" and "one/two steps below". Do not mix
  equations from one code with tables from another.
- Minimum curve length roughly 0.6·V (m, V km/h) for appearance (gated: unconfirmed, source is paywalled or blocked).
- Grades: maximum per class and terrain (e.g. freeways typically 3–6% (gated: unconfirmed, source is paywalled or blocked)); minimum
  ~0.3–0.5% on kerbed roads for drainage (gated: unconfirmed, source is paywalled or blocked).

## 6. Coordinate plan and profile
- Horizontal curves should **lead** and be longer than vertical curves; ideally the
  two coincide.
- Avoid a sharp horizontal curve starting at or just beyond a crest (hidden curve), or
  at the bottom of a long downgrade.
- Avoid broken-back curves and short tangents between same-direction curves.

## Verify
- [ ] Design (or operating) speed is justified and consistent along the route.
- [ ] Every horizontal radius meets the chosen code's minimum for its e and f, with e distributed per the code method.
- [ ] Superelevation runoff respects maximum relative gradients and drains at the 0% section.
- [ ] Crest and sag K values meet SSD (and headlight) requirements from the same code.
- [ ] Sight lines on horizontal curves clear barriers, cuttings and vegetation.
- [ ] Plan/profile coordination reviewed in 3D or a drive-through for hidden curves and dips.
