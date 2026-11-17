---
id: creative-arts.circus-arts.circus-act-creation.design-factors-and-wll-selection-for-circus-rigging
name: design-factors-and-wll-selection-for-circus-rigging
category: creative-arts
field: circus-arts
product: circus-act-creation
tags: [circus-act-creation, circus-arts, rigging-load-calculation, rigging-math, design-factor, wll-selection, working-load-limit, minimum-breaking-strength, hardware-selection, rigging-standards]
level: advanced
status: draft
description: "Choose rigging hardware for a circus act from its working load limit: MBS vs WLL, typical design factors by component, de-rating for hitches and angles, and documenting the choice."
sources: ["ASME B30.9 Slings and B30.26 Rigging Hardware - design factor provisions", "ANSI E1.43 Performer Flying Systems - https://tsp.esta.org", "Harry Donovan, Entertainment Rigging (2002)", "Manufacturer catalogues (Crosby, CM, Petzl) for rated loads"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Design factors and WLL selection for circus rigging

**Goal:** select each component so its rated working load limit covers the act's
calculated peak, with the design factor the applicable standard or rigger requires.

## Definitions
- **MBS** (minimum breaking strength): failure load of a new component.
- **Design factor (DF)**: MBS / WLL, built into the manufacturer's WLL rating.
- **WLL**: the maximum load the manufacturer allows in normal service.
Compare your **calculated load** to the **WLL**, not to the MBS.

## Typical design factors (check the specific product and standard)
- Wire rope slings: 5:1 (ASME B30.9).
- Synthetic round slings / web slings: 5:1 (ASME B30.9).
- Shackles: commonly 5:1 or 6:1 depending on manufacturer.
- Climbing/life-safety carabiners: rated by MBS in kN, often no WLL marked; riggers apply
  their own factor.
- Entertainment and performer-flying practice often applies additional factors on top
  for people and overhead audiences; ANSI E1.43 and local codes set the requirement.
  *Confirm the factor with the rigger and the standard in force.*

## De-rating
- **Choker hitch** on a sling: capacity reduced (often to about 80% of vertical; less at
  sharp choke angles).
- **Basket hitch**: up to 2x vertical only when legs are vertical; reduce with angle.
- **Sling angle**: tension rises as legs spread (see bridle math).
- **Edges**: synthetic slings over sharp edges lose most of their strength - always pad.
- **Temperature, chemicals, wear**: per manufacturer tables.

## Selection procedure
1. Calculate the peak load at each component (dynamic factor, bridle split).
2. Apply hitch and angle de-rating to the component's WLL.
3. Choose a component whose de-rated WLL is at least the peak load (rigger's extra factor
   applied if required).
4. Record component, WLL, de-rating and load in the rigging plot.

## Gotchas
- The chain is only as strong as the weakest component - including the anchor.
- Mixed units: convert everything to kN (1 kN = about 102 kgf).
- Unmarked hardware has no WLL: do not use it.

## Verify
- [ ] Every component's de-rated WLL meets its calculated load.
- [ ] Design factor source documented.
