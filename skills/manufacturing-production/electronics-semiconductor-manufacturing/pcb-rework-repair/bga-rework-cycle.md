---
id: manufacturing-production.electronics-semiconductor-manufacturing.pcb-rework-repair.bga-rework-cycle
name: bga-rework-cycle
category: manufacturing-production
field: electronics-semiconductor-manufacturing
product: pcb-rework-repair
tags: [pcb-rework-repair, bga, bga-rework, rework-station, hot-air, infrared-rework, ir-rework, ersa, pace, metcal, jovy, site-dressing, solder-wick, desoldering, reballing, flux, preheat, bottom-heater, thermocouple, x-ray-inspection, ipc-7711, ipc-7721, pad-repair, lifted-pad, msd-bake, j-std-033, pcba, repair]
level: advanced
status: draft
description: "Remove and replace a BGA on an assembled board: bake, profile the rework station, remove, dress the site without lifting pads, place, reflow and X-ray, following IPC-7711/7721 practice."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# BGA rework cycle

**Goal:** replace a BGA so the board is as reliable as a first-pass build — no lifted
pads, no overheated neighbours, no head-in-pillow — and prove it with X-ray.
IPC-7711/7721 is the reference for rework and repair methods; the customer contract
usually says whether reworked boards are acceptable at all and how many cycles a board
may see.

## 1. Before you heat anything
- **Authorisation:** is rework allowed on this product/class, and has this board been
  reworked before? Many specs limit heat cycles per location.
- **Bake** the board (and the replacement part if it is out of floor life) to drive
  out moisture; a wet board can delaminate or "popcorn" under local heat. Typical
  bakes run many hours at ~125 °C for bare components or lower temperatures for
  assemblies with heat-sensitive parts — *follow J-STD-033 and the site procedure*.
- **Profile the rework station** on a scrap board of the same assembly with a
  thermocouple under the BGA (drilled from the back into a ball/pad), plus TCs on
  neighbours. You are re-creating the reflow window (TAL, peak) locally.
- Shield heat-sensitive neighbours (Kapton tape, reflective shields) and remove any
  that cannot be shielded.

## 2. Removal
1. Apply bottom-side preheat to bring the whole board up gradually — this is what
   prevents warpage and lifted pads; top heat alone on a thick board is the classic
   failure.
2. Run the removal profile; lift with the station's vacuum pickup **only after**
   all balls are molten (the profile TC tells you, not a timer you guessed). Prying
   tears pads.

## 3. Site dressing
- Remove residual solder with a wide blade/solder wick and flux, or a non-contact
  scavenger. Low pressure, wick moved with the iron, never scrubbed. Lifted pads at
  this step are the most common rework damage.
- Clean flux residue with the specified solvent; inspect pads under magnification
  for damage, mask damage between pads, and flatness.
- Damaged pad → pad repair per IPC-7721 (bonded replacement pad), only if allowed
  for the class; otherwise the board is scrap.

## 4. Placement and reflow
1. Apply flux (tacky flux) or print paste with a mini-stencil — follow the site
   method; paste gives better standoff on some packages.
2. Align with the split-vision optics (balls vs pads overlaid), place.
3. Reflow with the profiled recipe, bottom heater on, gentle cooling.
4. Do not move the board until it has cooled below solidus.

## 5. Inspection
- **X-ray**: bridging, missing balls, voids percentage, and size uniformity (an
  oddly small/oval ball can hint at an open or head-in-pillow).
- Visual on the visible outer row (endoscope/side-view camera).
- Electrical test: the original failing test plus anything the rework could have
  disturbed nearby.
- Record: location, cycle count, profile, operator, inspection result — the board's
  traveller must show it has been reworked.

## Reballing
Reballing a removed BGA (to reuse it) is possible with a ball stencil, but many
customers forbid it for production; check before doing it.

## Gotchas
- Lead-free boards and mixed-alloy rework (leaded part on lead-free board, or vice
  versa) need a decision on alloy compatibility — don't improvise.
- Nearby capacitors on the board's back side under the BGA may reflow and drop if
  bottom heat is aggressive.
- Too much flux causes voids and residue under the part; too little gives
  non-wetting.
- Underfilled BGAs need underfill removal first — a much harder job.

## Verify
- [ ] Profile measured on this assembly with a TC under the part.
- [ ] Pads intact after dressing (inspected under magnification).
- [ ] X-ray shows no bridges/opens; voids within spec.
- [ ] Board passes the failing test and is recorded as reworked.

*Draft: bake times and void limits are site/customer-specific and not stated
numerically here on purpose; consult J-STD-033 and the contract.*
