---
id: repair-maintenance.consumer-electronics-repair.soldering-rework-equipment.iron-and-hot-air-smd-rework
name: iron-and-hot-air-smd-rework
category: repair-maintenance
field: consumer-electronics-repair
product: soldering-rework-equipment
tags: [soldering-rework-equipment, soldering-iron, hot-air-station, rework-station, smd-rework, through-hole, desoldering, bga-reflow, preheater, flux, no-clean-flux, solder-wick, desoldering-braid, leaded-solder, lead-free-solder, sac305, low-melt-solder, chipquik, kapton-tape, tip-tinning, hakko, jbc, quick-861dw, t12, ts100, esd, fume-extraction]
level: practitioner
status: draft
description: "Set up and use a soldering iron, hot-air station and preheater for through-hole and SMD removal and replacement: temperatures, airflow, flux, tip care, shielding and BGA reflow."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Iron and hot-air SMD rework — settings and technique

**Goal:** remove and replace through-hole and surface-mount parts (passives, QFN,
SOIC, connectors, small BGAs) without lifted pads, cooked plastics or cold joints,
using a temperature-controlled iron, a hot-air station and, for big boards, a preheater.

## 1. Bench and safety
- ESD mat and wrist strap to the same ground point; anti-static tweezers. Unplug
  mains and **disconnect the battery** before any heat goes near a board.
- Fume extraction at the work, not across the room: rosin flux smoke is a respiratory
  sensitiser. Wash hands after handling leaded solder; no food on the bench.
- Hot-air nozzles stay hot for minutes: park the handle in its cradle (most stations
  cool down automatically when docked).

## 2. Iron settings and tip care
| Job | Tip | Set point |
|---|---|---|
| 0402–0805 passives, fine pins | conical/bevel 0.8–1.2 mm, or knife | 320–350 °C leaded, 350–370 °C lead-free |
| Drag soldering QFP/SOIC | hoof/bevel 2–3 mm | 330–360 °C |
| Ground planes, connectors, through-hole | chisel 2.4–3.2 mm | 360–400 °C |

- The **tip size** moves heat, not the dial. If a joint takes over ~3 s, go to a
  bigger tip before going hotter.
- Keep the tip **tinned**; wipe on brass wool, re-tin before docking. Dry tips
  oxidise black and stop wetting. Recover with tip tinner paste, never by filing.
- Cartridge irons (JBC C245/C210, Hakko T12, Pinecil/TS100 clones) recover faster
  than older element-behind-tip designs, which matters on multilayer boards.

## 3. Flux and solder
- Use a tacky no-clean or rosin gel flux (syringe) for everything; more flux is
  almost always the fix for bridges and spiky joints.
- Factory boards are usually lead-free (SAC305, melts ~217–220 °C). **Mix in leaded
  63/37 (183 °C)** or a low-melt alloy (Chip Quik type, ~58–140 °C) to remove stubborn
  parts at lower temperature, then wick it all off so the low-melt alloy does not stay
  in the new joint (low-melt alloys are weak and brittle).
- Solder wick: add flux to the braid, lay it on the pad, press the iron on top,
  lift both together. Dragging braid tears pads.

## 4. Hot-air removal and placement
1. **Shield** neighbours: Kapton tape plus aluminium foil over plastic connectors,
   crystals, electrolytics and camera modules. Remove plastic covers and shields first.
2. Flux the part. Typical start: **350–380 °C, low-to-mid airflow** (about 30–50 % on
   a Quick 861DW-class station), nozzle 1–2 cm above the part, moving in small circles.
   Tiny passives: lower airflow or they blow away.
3. Wait for the flux to go thin and the solder to shine, then nudge with tweezers.
   **Never lever** — if it resists, it is not molten and the pads will come with it.
4. Clean pads with braid, IPA (99 %) and a brush. Inspect for lifted or torn pads
   before placing anything.
5. Place: tin pads lightly (or paste), flux, align, heat until the part self-centres
   via surface tension. QFN ground pads: thin solder layer only, or the part floats.

## 5. Preheat and BGA reflow
- Boards over ~1.6 mm or with heavy copper: preheat the underside to **120–150 °C**
  (bottom heater or hotplate) so the top heat only has to add the last ~100 °C.
  This is the single biggest cure for lifted pads.
- BGA removal: preheat, flux around the edge, heat evenly with a large nozzle, lift
  with a vacuum pick when the chip floats on a gentle touch. Reballing needs a stencil
  and is covered under board-level microsoldering
  (repair-maintenance.consumer-electronics-repair.board-level-microsoldering.microscope-ic-swap-and-pad-jumper-repair).
- "Reflowing" a failing GPU/BGA in place is often a temporary fix; cracked balls or
  dead silicon return within weeks. (Draft note: report as a diagnostic, not a repair.)

## Gotchas
- Display of station temperature is not tip temperature; check with a tip
  thermometer (Hakko FG-100 class) when results drift.
- Hot air over a Li-ion cell, a flex cable or an OLED panel will damage it in seconds —
  remove or heavily shield them.
- Underfilled chips (common in phones) need underfill softened and picked away before
  lift; see the microsoldering skill.
- Moisture in old boards can delaminate ("popcorn") under fast heat — bake at
  ~100 °C for some hours first (Draft note: bake times vary by board and are not
  confirmed here).

## Verify
- [ ] Joints are smooth, concave fillets, wetted onto the pad; no bridges under 10x magnification.
- [ ] Neighbouring parts and plastics unmarked; no lifted or darkened pads.
- [ ] Continuity / no short to ground on the reworked rail, measured before power-up.
- [ ] Flux residue cleaned with IPA where it could be conductive or sticky.
- [ ] Device powers and the reworked function works.
