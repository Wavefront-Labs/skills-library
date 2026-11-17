---
id: creative-arts.circus-arts.aerial-arts.dynamic-load-factors-for-aerial-points
name: dynamic-load-factors-for-aerial-points
category: creative-arts
field: circus-arts
product: aerial-arts
tags: [aerial-arts, circus-arts, aerial-rigging, dynamic-load-factor, working-load-limit, aerial-point-rating, design-factor, minimum-breaking-strength, shock-load, rigging-math, drops, beats]
level: advanced
status: draft
description: "Estimate peak loads from aerial drops and beats, relate them to WLL, MBS and design factor, and decide what point rating to ask a rigger for. Orders of magnitude, not a design."
sources: ["ANSI E1.43 Performer Flying Systems - https://tsp.esta.org", "Harry Donovan, Entertainment Rigging (2002) - dynamic loads and design factors", "ETCP Arena and Theatre Rigger candidate handbooks - https://etcp.esta.org", "FEDEC aerials manual safety chapter - https://www.fedec.eu"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dynamic load factors for aerial points

**Goal:** understand why an aerial point rated for "a person" is not enough, and be able
to give a rigger a realistic peak load so they can rate the point and chain.

## The vocabulary
- **MBS / breaking strength**: load at which a new component fails in a lab.
- **Design factor (DF)**: MBS divided by the allowed working load. Lifting slings are
  typically rated at 5:1; performer-flying and life-safety practice uses higher factors.
  Check the current ANSI E1.43 edition or local equivalent (EN 17206 in Europe) for the
  figure your rigger must apply.
- **WLL**: the maximum load in normal use = MBS / DF. Marked on the part.
- **Dynamic factor**: peak force divided by static weight during a move.

## Why aerial loads are dynamic
A body that falls and is arrested by fabric or a hoop decelerates over a short distance.
Peak force = mass x (g + deceleration). The shorter the stopping distance and the
stiffer the apparatus, the higher the peak.
- Static hang: about 1x body weight.
- Beats, swings, small drops on stretchy fabric: commonly measured around 2-4x.
- Large drops on low-stretch apparatus (lyra, straps, static trapeze), duo work, or a
  partner catching a partner: commonly quoted in the 5-10x range.
These are orders of magnitude from published measurements and rigger practice. *Exact
figures depend on apparatus stretch, technique and height; ask for load-cell data if
the act is new.*

## Worked estimate
Duo lyra, performers 60 kg and 75 kg, hoop and hardware 10 kg.
- Static: 145 kg, about 1.42 kN.
- Assume a dynamic factor of 6 for drops: about 8.5 kN peak.
- Every component in the chain must have a WLL at or above that peak, i.e. with a 10:1
  design factor an MBS of about 85 kN. That is why aerial carabiners stamped 25-30 kN
  are not enough on their own for dynamic duo work, and why riggers often specify
  large shackles and doubled slings.

## What to give the rigger
- Number and weight of performers, apparatus weight.
- Worst move: largest drop height, any catches or partner drops.
- Whether the apparatus swings (horizontal load components) or spins.
- Measured peak from a load cell if you have one (inline dynamometer at the swivel
  during rehearsal is the gold standard).

## Gotchas
- Swinging apparatus adds horizontal force; the anchor sees an angled load.
- Two points bridled together share load unequally unless the bridle is designed for it
  (see bridle math in circus-act-creation).
- Fatigue: hardware loaded dynamically every day ages faster than its lab rating suggests.

## Verify
- [ ] You can state static load, assumed dynamic factor and resulting peak in kN.
- [ ] Every link's WLL meets the peak; the anchor rating covers the peak plus direction.
- [ ] The rigger's design factor is documented with the standard it comes from.
