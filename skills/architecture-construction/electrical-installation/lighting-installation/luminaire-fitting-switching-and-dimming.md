---
id: architecture-construction.electrical-installation.lighting-installation.luminaire-fitting-switching-and-dimming
name: luminaire-fitting-switching-and-dimming
category: architecture-construction
field: electrical-installation
product: lighting-installation
tags: [electrical-installation, lighting-installation, luminaire, light-fixture, downlight, ceiling-rose, two-way-switching, intermediate-switch, three-way-switch, four-way-switch, switch-loop, dimmer, leading-edge, trailing-edge, led-driver, 0-10v, dali, ic-rated, ip-rating, bathroom-zones, emergency-lighting, class-ii, lockout-tagout, nec, bs-7671]
level: practitioner
status: draft
description: "Fit luminaires and downlights safely, wire one-way/2-way/intermediate (3-way/4-way) switching, match dimmers to LED drivers, and connect emergency fittings."
sources: ["NFPA 70 National Electrical Code (NEC) Articles 404 and 410", "BS 7671 Requirements for Electrical Installations", "AS/NZS 3000 Wiring Rules", "BS 5266-1 Emergency lighting"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Luminaire fitting, switching and dimming

**Goal:** hang or recess a luminaire so it is securely supported, correctly rated for its
location, switched in the line conductor from the right places, and dims smoothly
without flicker — and keep emergency fittings genuinely independent of the switch.

> **Licensed, jurisdiction-specific work.** Fixed lighting wiring generally needs a
> licensed electrician; bathroom, outdoor and emergency lighting have extra rules. Values
> below are typical and labelled; confirm against your edition of the wiring rules and
> the luminaire instructions.

## 1. Isolate — lighting circuits bite
1. Turn the light switch off **and** isolate the circuit at the board; lock off and tag.
2. Prove the tester, test dead at the fitting (L–N, L–E, N–E, and every conductor in
   the box — switch loops and through-feeds), re-prove the tester.
3. Expect **more than one circuit** in a ceiling box or switch box (looped feeds,
   2-way switching from another circuit, a "borrowed neutral"). If anything reads live,
   find its source before continuing.

## 2. Choose and fix the luminaire
- **Support:** fix to a joist, noggin/blocking or a box rated for the weight. US: a
  standard outlet box supports luminaires up to 50 lb (23 kg); ceiling fans need a
  fan-rated box.
- **Recessed downlights:** cut the hole to the maker's size; keep clearance from thermal
  insulation unless the fitting is IC-rated (US) or insulation-coverable; restore the
  ceiling's fire rating with rated downlights or hoods where the ceiling is a fire barrier.
- **Location rating:** bathrooms are zoned (UK/AU zones 0/1/2; US "damp/wet location"
  listing). UK zone 1 typically needs at least IPX4 and 30 mA RCD protection;
  outdoor fittings commonly IP44–IP65.
- **Class I** fittings must be earthed; **Class II** (double-insulated) need no earth but
  the circuit protective conductor is still terminated (in a connector), not cut off.
- Use heat-resistant flex/sleeving at hot lampholders; keep the driver within its
  temperature rating and accessible for replacement.

## 3. Switching
- Switches always break the **line** conductor. Re-identify a switch-loop "neutral"
  colour with line tape.
- **One-way:** line in → switch → switched line to luminaire.
- **Two-way (US three-way):** common (COM) of switch 1 gets the line feed, two
  strappers/travellers (L1, L2) link the switches, common of switch 2 feeds the lamp.
- **Intermediate (US four-way):** inserted in the travellers between the two two-way
  switches; any number can be added.
- **Neutral at the switch:** US NEC now generally requires a grounded conductor at switch
  locations (for smart switches); good practice everywhere.

## 4. Dimming
- Match dimmer to **driver** type: leading-edge (TRIAC/phase-forward) vs trailing-edge
  (phase-reverse); most integral LED lamps prefer trailing-edge. Check the lamp/driver
  maker's compatibility list.
- Respect **minimum load** — too few LEDs causes flicker or ghosting (glowing when off);
  derate the dimmer's maximum for LED (often to a fraction of its incandescent rating).
- Commercial: **0–10 V** (control pair must be segregated/rated as required, polarity
  matters), **DALI** (addressable two-wire bus, polarity-free), or DMX for theatrical.

## 5. Emergency lighting
- Feed self-contained fittings with an **unswitched permanent live** from the same
  local lighting circuit, so a local circuit failure triggers emergency mode.
- Maintained (lit always) vs non-maintained (lit only on failure).
- Typical rated duration: UK 3 h for most premises, US 90 min (unverified — confirm
  against your edition of the wiring rules and fire code).
- Fit a key test switch; record a full-duration test on commissioning.

## Gotchas
- Switching the neutral leaves the lampholder live with the switch off.
- Mixing circuits in a 2-way arrangement trips RCDs and defeats isolation.
- Non-IC downlights buried in insulation overheat; IC/non-IC labels differ by region.
- Emergency fitting fed from the switched live goes into emergency mode, draining its
  battery, every time someone switches the lights off.

## Verify
- [ ] Every conductor in the box proved dead before work; source of any extra circuit known.
- [ ] Fitting supported by a rated box/fixing; IP and IC/insulation rating suits the location.
- [ ] Switches break line; 2-way/intermediate operates from every position.
- [ ] Dimmer type and load range match the driver; no flicker at low end; no glow when off.
- [ ] Emergency fittings on unswitched live; duration test recorded.
- [ ] Earth continuity and polarity tested at each point.
