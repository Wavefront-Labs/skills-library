---
id: manufacturing-production.electronics-semiconductor-manufacturing.reflow-wave-soldering.reflow-profile-development-and-defect-diagnosis
name: reflow-profile-development-and-defect-diagnosis
category: manufacturing-production
field: electronics-semiconductor-manufacturing
product: reflow-wave-soldering
tags: [reflow-wave-soldering, reflow, reflow-profile, thermal-profiling, profiler, kic, datapaq, thermocouple, tal, time-above-liquidus, peak-temperature, ramp-rate, soak, ramp-to-spike, sac305, lead-free, j-std-020, voiding, tombstoning, head-in-pillow, solder-balling, graping, cold-joint, wave-soldering, selective-soldering, nitrogen-reflow, pcba, smt]
level: practitioner
status: draft
description: "Build and verify a lead-free reflow profile with a thermocouple profiler, read the curve (ramp, soak, TAL, peak), and map common solder defects back to profile or print causes."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reflow profile development and defect diagnosis

**Goal:** a profile that puts *every* joint on the board inside the paste's process
window — hottest part not over its rating, coldest joint fully reflowed — and the
ability to tell a profile defect from a print or design defect.

## 1. Start from the paste datasheet, not the last job
The solder paste datasheet gives the window: typical SAC305 targets (check yours) are
roughly a ramp of 1–3 °C/s, a soak or ramp-through of ~150–200 °C, **time above
liquidus (217–220 °C) of ~45–90 s**, and **peak ~235–250 °C** at the joint. Component
limits (J-STD-020 classification, often 245–260 °C peak by package size) cap the top.
Your window is the overlap.

## 2. Instrument a real board
- Use a populated scrap board of the actual assembly, not a bare one — thermal mass
  is the point.
- Attach thermocouples (high-temp solder, aluminium tape or Kapton+adhesive; drilled
  into a BGA ball is the gold standard for big BGAs) at:
  1. the largest thermal mass (big BGA centre, shielded can, connector with ground pins),
  2. the smallest / most exposed part (board edge 0402),
  3. a heat-sensitive part (electrolytic cap, connector plastic, LED),
  4. a ground-plane-heavy area.
- Run the profiler (KIC, Datapaq, ECD etc.) through the oven at the production
  conveyor speed.

## 3. Read and adjust
- **Delta-T** between hottest and coldest TC at peak is the key number. Large delta →
  lengthen soak to equalise, slow the conveyor, or raise lower-zone (bottom) heaters.
- Cold joint short on TAL → raise the last two zones or slow the belt; small parts
  over peak → lower top heater in peak zone, rely more on time than temperature.
- Change one thing at a time; re-run; save the profile with the oven recipe name,
  board ID, TC map and date.
- Many profilers have a "prediction" mode that suggests recipe changes — useful,
  but verify with a real run.

## 4. Defect → likely cause (start here, then confirm)
| Defect | First suspects |
|---|---|
| Tombstoning (small chips) | Unequal pad heating/pad sizes, fast ramp through liquidus, offset placement |
| Solder balls / mid-chip balls | Paste on mask (print offset, smear), too fast ramp (solvent spatter), excess paste |
| Head-in-pillow (BGA) | Package/board warpage at peak, oxidised balls, flux exhausted by long soak |
| Graping / grainy joints | Flux exhausted — too long or too hot soak, paste too old on stencil |
| Voiding (QFN thermal pads) | Paste volume and windowpane aperture design, outgassing; profile tweak helps less |
| Cold / incomplete reflow | Low TAL/peak at high-mass location |
| Bridging | Print first (excess paste, slump), then placement pressure |

Rule of thumb: **most "reflow" defects are print defects.** Check SPI data before
touching the oven.

## 5. Wave and selective, briefly
- Wave: flux amount and coverage, preheat so the top side reaches the flux activation
  temperature (spec'd on flux datasheet), contact time typically a few seconds, board
  angle, and pot temperature/alloy maintenance (copper build-up in lead-free pots is
  analysed periodically). Bridging on trailing leads → solder thieves, conveyor angle.
- Selective: nozzle size, dwell per joint, nitrogen, and barrel fill on thick boards
  (IPC class 2/3 hole-fill requirements).

## Verify
- [ ] Every TC location inside the paste window (TAL, peak, ramp) — not just the average.
- [ ] No component over its rated peak.
- [ ] Profile saved and linked to the recipe; re-profiled at the site's interval or after
      oven maintenance, a new board revision or a conveyor-speed change.
- [ ] Defect fix confirmed by AOI/X-ray on the next boards, not one sample.

*Draft: numeric windows are typical for SAC305 and vary by paste vendor; always defer
to the datasheet. Wave/selective section is overview-level.*
