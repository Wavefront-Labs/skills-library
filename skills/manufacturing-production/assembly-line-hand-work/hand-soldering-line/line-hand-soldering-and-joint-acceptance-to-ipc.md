---
id: manufacturing-production.assembly-line-hand-work.hand-soldering-line.line-hand-soldering-and-joint-acceptance-to-ipc
name: line-hand-soldering-and-joint-acceptance-to-ipc
category: manufacturing-production
field: assembly-line-hand-work
product: hand-soldering-line
tags: [hand-soldering-line, assembly-line-hand-work, hand-soldering, soldering, ipc-a-610, j-std-001, ipc-class-2, ipc-class-3, through-hole, tht, smd-touch-up, solder-joint-inspection, wetting, fillet, hole-fill, barrel-fill, solder-bridge, cold-joint, flux, no-clean-flux, lead-free, sac305, soldering-iron, tip-tinning, esd, msd, rework, selective-solder, touch-up]
level: practitioner
status: draft
description: "Hand-solder and touch up boards on a production line to IPC J-STD-001/IPC-A-610: tip and temperature choice, through-hole and SMD technique, flux control, and accept/reject calls on joints."
sources: ["IPC J-STD-001 Requirements for Soldered Electrical and Electronic Assemblies", "IPC-A-610 Acceptability of Electronic Assemblies"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Line hand-soldering and joint acceptance to IPC

**Goal:** make and inspect solder joints at a line station — after wave/selective
soldering, for hand-placed through-hole parts, or SMD touch-up — that meet the
**product's IPC class**, at line pace, without damaging the board. J-STD-001 is the
*process* requirement; IPC-A-610 is the *visual acceptance* standard. Both are paid
standards; this skill summarises the practice, not their text. Formal certification
(IPC CIS) is commonly required for line operators — this does not replace it.

For bench rework and hot-air component swaps, see
repair-maintenance.consumer-electronics-repair.soldering-rework-equipment.iron-and-hot-air-smd-rework.

## 1. Know the class
- **Class 1** general, **Class 2** dedicated service (most commercial/industrial),
  **Class 3** high performance (medical, aerospace, military). The same joint can be
  acceptable for Class 2 and a defect for Class 3 (e.g. through-hole vertical fill
  minimums are stricter). Check the traveller/work order for the class.

## 2. Station setup
- ESD: grounded mat, wrist strap tested at shift start, ESD-safe tools. Moisture-
  sensitive parts (MSD) only within their floor life.
- **Iron:** temperature-controlled station. Typical tip setpoints for lead-free (SAC305)
  are roughly 340–380 °C; tin-lead lower. Use the lowest that gives a joint in a few
  seconds — your site's process spec governs. Verify tip temperature with a tip
  thermometer at the frequency your process sets.
- **Tip:** largest tip that fits the joint (chisel for most through-hole). Good heat
  transfer beats more temperature. Keep it **tinned**; clean on brass wool, re-tin
  before parking. A dull grey tip won't wet.
- **Solder and flux:** the alloy and flux type specified for the product (usually
  no-clean cored wire). Don't mix lead-free and tin-lead on one board.

## 3. Through-hole technique
1. Touch the tip to **both pad and lead** at once (heat both surfaces).
2. Feed solder into the joint (opposite the tip, not onto the tip) — it should flow
   and wick into the barrel within ~1–3 s.
3. Remove solder, then the iron. Don't move the part while it solidifies.
4. Target: concave fillet, good wetting to lead and pad (low contact angle), lead
   outline visible, barrel fill to the class requirement.
Heavy ground-plane joints need a bigger tip or board preheat, not a hotter iron held
longer (that lifts pads).

## 4. SMD touch-up
- Chip components: tack one end, then solder the other, then reflow the first.
- Fine-pitch bridges: add flux, drag a clean tinned tip along the leads, or use wick.
  Excess flux residue on no-clean processes may need cleaning if the spec says so.
- Don't touch-up joints that are acceptable: extra heat cycles damage boards and IPC
  treats unnecessary rework as a process issue.

## 5. Accept or reject — common calls
| Condition | Usual call |
|---|---|
| Smooth, concave fillet, wetted to both | Accept |
| Bridge between conductors | Defect (all classes) |
| Non-wetting / dewetting (balled-up solder) | Defect |
| Cold / disturbed joint (grainy, cracked) | Defect |
| Insufficient barrel fill | Depends on class — check the table |
| Solder balls/splashes loose | Defect if they violate spacing or are not entrapped |
| Pad lifted / board burnt | Defect — escalate, likely scrap/engineering disposition |
Use the magnification the standard and your process call for; don't inspect
everything at maximum zoom (that reveals irrelevant features) or by naked eye only.

## 6. Line discipline
- Work to the routing: which joints the station owns.
- Record rework against the board serial in the MES/traveller; repeated touch-up of
  the same joint is a wave/selective process problem to report upstream.
- Fume extraction at the tip; wash hands before eating (lead, flux).

## Verify
- [ ] Product class known; certification current.
- [ ] ESD checked; tip temp verified; tip tinned and the right size.
- [ ] Joints made in a few seconds with no pad lift.
- [ ] Each joint inspected against the class criteria; defects recorded by serial.

*Uncertain: temperatures and class-specific fill limits are summarised from general
practice — check the current IPC revision and your process spec.*
