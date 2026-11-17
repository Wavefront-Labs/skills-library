---
id: repair-maintenance.consumer-electronics-repair.board-level-microsoldering.microscope-ic-swap-and-pad-jumper-repair
name: microscope-ic-swap-and-pad-jumper-repair
category: repair-maintenance
field: consumer-electronics-repair
product: board-level-microsoldering
tags: [board-level-microsoldering, microsoldering, stereo-microscope, ic-replacement, bga, reballing, reball-stencil, underfill, underfill-removal, pad-repair, trace-repair, jumper-wire, enamelled-wire, magnet-wire, uv-solder-mask, uv-curing, fibreglass-pen, sandwich-board, logic-board, tristar, charging-ic, backlight-ic, preheater, flux, esd]
level: advanced
status: draft
description: "Under the microscope: remove underfilled ICs, reball and refit BGAs, rebuild torn pads and broken traces with jumper wire and UV mask on dense phone and laptop logic boards."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Microscope IC swaps, pad rebuilds and jumper wires

**Goal:** replace a failed IC on a dense logic board (phone charging/backlight ICs,
laptop power ICs, small BGAs) and repair the pads and traces that come with it, so
the board passes the same measurements as a known-good one.

## 1. Setup
- Stereo microscope with 7–45x zoom and a ring light; a 0.5x Barlow lens gives more
  working distance under a hot-air nozzle.
- Board holder that grips the edges; preheater for thick boards; fine tweezers
  (curved and straight), scalpel #11, 0.1 mm enamelled copper wire, UV-curing solder
  mask, UV torch, fibreglass pen, 99 % IPA, tacky flux, low-melt solder paste.
- ESD grounding throughout. Battery and all flexes disconnected; shield cameras,
  Face ID/fingerprint parts and the CPU with Kapton/foil.
- Iron and air settings: see
  repair-maintenance.consumer-electronics-repair.soldering-rework-equipment.iron-and-hot-air-smd-rework.

## 2. Removing an underfilled IC
1. Measure and record diode-mode values on the IC's key nets first, for comparison later.
2. Preheat the board to ~150 °C. Flux heavily around the chip.
3. Heat with hot air (~380 °C, low airflow) until solder liquefies; the underfill
   (epoxy around the balls) softens but does not melt.
4. Slide a thin blade or a pry tool under one edge and lift gently **only when** the
   chip moves freely. Forcing it rips pads, especially the small NC/test pads.
5. Underfill remaining on the board: soften with heat and scrape **away from the pads**
   with the blade or a fibreglass pen at low angle, a little at a time. Some techs use
   underfill-softening solvents first. (Draft note: solvent choice and dwell times
   vary; not confirmed here.)
6. Level the pads with fresh leaded solder and braid; clean with IPA; inspect every pad.

## 3. Reballing and refitting a BGA
1. Clean the chip's old balls off with braid and flux until pads are flat and bright.
2. Fix the chip in a reball jig or align a matching stencil by eye under the scope.
3. Spread low-melt or leaded paste across the stencil, scrape flush, heat gently
   (~300 °C, low airflow) until balls form. Let cool, remove stencil, reflow briefly
   with flux to round the balls.
4. Flux the board pads thinly, place the chip using the silkscreen corners and pin-1
   mark, heat until it **settles and self-aligns** — a tiny nudge should spring back.
5. Do not re-underfill until the repair is tested working.

## 4. Pad and trace repair
- **Torn pad that has a trace:** scrape solder mask off the trace 1–2 mm back,
  tin it, solder a short piece of 0.1 mm enamelled wire from the trace to the
  component pin or ball position.
- **Torn pad that is via-only:** check the boardview for where the net goes and
  jumper to the nearest exposed point on that net (a cap pad or test point).
- Unused/NC pads (check the schematic) can be left missing.
- Cover the repaired area with UV mask, cure 1–2 minutes under UV, then scrape mask off
  only where a joint is needed. Mask also anchors jumper wires.
- Keep jumpers short and flat; long loops on high-speed lines (data, clock) cause
  faults. Never jumper RF or high-speed differential pairs casually.

## 5. "Sandwich" boards
Stacked phone boards are separated on a separator plate at ~165–180 °C. Clean and
re-tin the interposer, then reassemble with low-melt paste. Misalignment or a missed
ball causes intermittent faults later. (Draft note: plate temperature is from common
practice and depends on the paste/model.)

## Gotchas
- Wrong part revision: ICs that look identical can have different firmware or
  programming (e.g. some charge and audio ICs). Buy from a donor of the same board.
- Overheating the area kills nearby NAND or the CPU; work quickly and keep preheat
  on rather than turning top heat up.
- Pads that look fine can be detached underneath — push gently with a tweezer tip
  after cleaning.
- Flux under a BGA left uncleaned can conduct over time on high-impedance lines.

## Verify
- [ ] Diode-mode readings on the IC's nets match the pre-removal or known-good values.
- [ ] Every jumper is insulated with cured mask, short and fixed in place.
- [ ] The device powers, the target function works, and current draw is normal.
- [ ] No new faults on neighbouring functions (camera, Wi-Fi, sensors) after the heat.
- [ ] Repair passes a 30-minute load or charge test before reassembly.
