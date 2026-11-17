---
id: manufacturing-production.metal-plastics-fabrication-production.blow-moulding.stretch-blow-wall-distribution-control
name: stretch-blow-wall-distribution-control
category: manufacturing-production
field: metal-plastics-fabrication-production
product: blow-moulding
tags: [blow-moulding, blow-molding, stretch-blow-moulding, isbm, sbm, reheat-stretch-blow, pet, preform, preform-oven, ir-lamps, heating-profile, stretch-rod, preblow, final-blow, wall-thickness, section-weights, base-clearance, top-load, burst-test, leak-test, pearlescence, sidewall, extrusion-blow-moulding, ebm, parison, parison-programming, hdpe, sidel, krones, sipa]
level: practitioner
status: draft
description: "Control wall distribution on a PET stretch-blow machine: oven lamp profile, preblow timing and stretch rod, section weights and container tests, plus EBM parison programming."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Stretch-blow wall distribution control

**Goal:** bottles with material where it is needed — base, shoulder, label panel —
passing top-load, burst and base tests at full machine rate. Wall distribution comes
almost entirely from **where the preform is hot** and **when the preblow starts**.

## 1. How the material moves
In reheat stretch-blow (two-stage, e.g. Sidel, Krones, SIPA), a PET preform is heated
by IR lamp zones, stretched axially by a stretch rod and blown radially with low-pressure
**preblow** then high-pressure **final blow**. Hotter regions stretch more and end up
**thinner**; cooler regions stretch less and stay **thicker**. Each lamp zone maps to a
band of the preform and therefore a band of the bottle.

## 2. Measure, then adjust
- **Section weights**: cut the bottle into bands (base, lower body, panel, shoulder,
  neck) with a hot wire/section cutter and weigh each. Compare to the spec weights.
- **Wall thickness** with a magnetic ball gauge (Hall-effect, e.g. Magna-Mike-type) at
  defined points, especially the base and the thinnest panel area.
- Change **one lamp zone** at a time in small steps, then re-measure after the oven
  has stabilised (a few minutes).

## 3. Typical adjustments
| Problem | First adjustment |
|---|---|
| Heavy base / thin shoulder | More heat low on the preform (base zones), or earlier preblow |
| Thin base, base failures | Less heat near the gate/base zones; check stretch-rod gap to base |
| Thick shoulder ring | More heat in neck-adjacent zone, but protect the finish (cooling) |
| **Pearlescence** (white, hazy stretch marks) | Material too **cold** in that region — over-stretched |
| Haze/crystallinity (milky) | Material too **hot** — crystallising; reduce heat |
| Off-centre gate, uneven base | Stretch rod timing/centring, preform temperature balance across circumference (rotation) |
| Underfilled base/feet details | Final blow pressure or time too low, mould venting |

Preblow **timing (start position)** and **preblow pressure/flow** shift material up or
down: earlier/stronger preblow pushes material away from the base; later/weaker leaves
more in the base. Stretch-rod speed must stay ahead of the bubble.

## 4. Container tests
Per the customer spec, typically: **top-load** (vertical crush), **burst** (carbonated),
**base clearance** and **stress cracking** for CSD bottles, **volume/fill-point**, perpendicularity,
and **leak test** (often inline). Take samples per cavity/mould station — one bad mould
on a 20-cavity wheel hides in averages.

## 5. Preform handling
- Preforms must be at a stable temperature before the oven; cold preforms from an
  unheated warehouse shift the whole profile.
- Moisture in PET matters most at preform injection (where resin is dried), but preform age and storage
  conditions (dust, scratches, moisture) still affect blowing.
- Check preform lot/IV (intrinsic viscosity) changes — a different resin lot can
  need a re-profile.

## 6. Extrusion blow moulding (EBM), briefly
For HDPE/PP containers, a parison is extruded and blown. Wall distribution is set by
**parison programming** — a profile of die-gap openings along the parison length (often
dozens of points) — plus die shaping. Thin corners/handles → open the die gap at that
parison point. Pinch-off weld quality and flash trimming are the other key checks.

## Gotchas
- Lamp failures: a single dead lamp gives a band defect; check the lamp-current display.
- Ambient changes (summer/winter) shift the oven balance; re-check section weights.
- Speeding the machine up shortens heating time — profile again at the new rate.

## Verify
- [ ] Section weights per band within spec on every cavity/station sampled.
- [ ] Thinnest point above minimum wall.
- [ ] Top-load, burst/base and leak tests pass per plan.
- [ ] Profile recorded with preform lot and machine rate.

*Draft: test methods and values vary by brand owner spec; lamp-zone behaviour described
generally — machine HMIs differ.*
