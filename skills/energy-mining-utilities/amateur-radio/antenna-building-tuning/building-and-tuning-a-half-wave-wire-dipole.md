---
id: energy-mining-utilities.amateur-radio.antenna-building-tuning.building-and-tuning-a-half-wave-wire-dipole
name: building-and-tuning-a-half-wave-wire-dipole
category: energy-mining-utilities
field: amateur-radio
product: antenna-building-tuning
tags: [antenna-building-tuning, antenna, dipole, half-wave-dipole, inverted-v, wire-antenna, amateur-radio, ham-radio, hf-antenna, 468-over-f, swr, vswr, swr-meter, antenna-analyser, nanovna, rigexpert, resonance, coax, feedline, balun, 1-1-balun, choke, common-mode-current, end-insulator, centre-insulator, antenna-height, tree-launch, throw-line, overhead-power-lines, antenna-safety, trimming]
level: intro
status: draft
description: "Build, raise and tune a single-band HF half-wave dipole: cut length from 468/f, centre insulator and choke balun, safe raising away from power lines, and trimming for minimum SWR with an analyser."
sources:
  - "Standard amateur antenna references (e.g. ARRL Antenna Book, RSGB antenna guides): half-wave length formula and dipole practice, paraphrased"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Building and tuning a half-wave wire dipole

**Goal:** a cheap, efficient HF antenna that presents a good match to 50-ohm coax on
your chosen band, built so it survives the weather and tuned in a few iterations.

## 1. Cut the wire
- Approximate total length for a resonant half-wave wire dipole:
  **feet ≈ 468 / f (MHz)**, or **metres ≈ 142.6 / f (MHz)**. Each leg is half of that.
  Example: 14.2 MHz → about 33 ft (≈10.0 m) total, two ≈5 m legs.
- **Cut about 3–5% long**: you trim to resonance; adding wire back is harder than cutting.
  Insulated wire, nearby objects and height all shift resonance (insulation usually
  makes it resonate lower, so it ends up shorter).
- Wire: stranded copper or copper-clad steel of adequate strength; you need
  extra for wrapping at insulators.

## 2. Assemble
- **Centre:** a centre insulator or a 1:1 **current (choke) balun**. The balun or a
  coax choke (several turns of coax through ferrite, or coiled feedline) keeps RF off
  the outside of the coax shield. Without it, the coax radiates, the pattern skews,
  and you may get "RF in the shack" (tingles from the mic, interference).
- **Ends:** egg or dog-bone insulators; fold the wire back through and wrap it
  around itself rather than relying on a tight knot.
- **Weatherproof** the coax connector (self-amalgamating tape, then PVC tape over it).
  Water in coax is a slow, hidden failure.
- Use low-loss coax appropriate to the length and band; a strain relief so the coax
  weight doesn't hang from the solder joints.

## 3. Raise it safely
- **Stay well clear of power lines:** the antenna and the throw line must not be
  able to fall or swing onto them, even if a support breaks. Most fatal amateur
  antenna accidents involve power lines.
- Height: a horizontal dipole works best for DX at roughly a half-wavelength or more
  up; lower still works, favouring closer contacts (higher-angle radiation).
- An **inverted-V** (centre high on one support, ends sloping down) is fine and needs
  only one tall support; keep the included angle above roughly 90° and the ends out
  of reach of people (RF burns at the ends when transmitting).
- In trees: a throw weight or slingshot with a light line, then haul up a stronger
  rope; tie ends off with a pulley and counterweight or a bungee so the tree's movement
  doesn't snap the wire.

## 4. Tune
Use an **antenna analyser** (NanoVNA, RigExpert or similar) at the feedpoint end of
the coax, or a transceiver with an SWR meter at low power.
1. Sweep across the band and find the **frequency of minimum SWR**.
2. If minimum is **below** your target, the antenna is too long: shorten both legs
   equally. Shorten each leg by roughly the same proportion as the frequency error
   (e.g. 3% low → trim ~3% from each leg). If it's **above**, it's too short: add wire
   (or fold less back).
3. Fold the ends back on themselves rather than cutting until you're sure — easy to
   undo.
4. Re-raise to the same height each time; lowering to adjust changes the result.
5. Aim for SWR below ~1.5:1 at your favourite frequency; under 2:1 across most of the
   band is typical. Minimum SWR well above ~1.5 at resonance suggests a feedpoint
   impedance far from 50 ohms (very low height, nearby objects) or a bad connection.

## 5. Troubleshooting
- SWR changes when you touch or move the coax → common-mode current; add or improve
  the choke.
- SWR very high everywhere → open or shorted coax/connector. Check continuity.
- SWR drifts with rain → water ingress or wet insulators/trees.

## Verify
- [ ] Wire cut long from 468/f (142.6/f), legs equal.
- [ ] Choke balun at feedpoint; connectors weatherproofed; strain relief fitted.
- [ ] No way for antenna or lines to contact power lines; ends out of reach.
- [ ] SWR minimum moved onto target by equal trims, tested at final height.
- [ ] SWR stable when the coax is moved.
