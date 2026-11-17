---
id: manufacturing-production.cnc-machining-production.fanuc-cnc-control.offsets-macro-b-and-alarm-recovery
name: offsets-macro-b-and-alarm-recovery
category: manufacturing-production
field: cnc-machining-production
product: fanuc-cnc-control
tags: [fanuc-cnc-control, fanuc, fanuc-0i, fanuc-31i, cnc-control, mdi, work-offset, g54, g54-1, external-offset, tool-length-offset, g43, tool-geometry, tool-wear, wear-offset, cutter-radius-compensation, macro-b, custom-macro, system-variables, common-variables, 500-series-variables, alarm, overtravel, ps-alarm, reference-return, zero-return, parameter, parameter-write-enable, memory-backup, cnc-machining-production]
level: practitioner
status: draft
description: "Work a FANUC control in production: work and tool offsets (geometry vs wear), Macro B variables for part counters and probing logic, safe parameter changes, and recovering from common alarms."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Offsets, Macro B and alarm recovery on a FANUC control

**Goal:** set up and hold size on a FANUC 0i/30i-series control with offsets the next
shift understands, use macros where they pay, and get out of alarms without making
it worse.

*Draft: generic FANUC behaviour; machine builders that fit FANUC controls (Haas and Okuma use their own controls)
add their own M-codes, screens and alarms. Parameter numbers
vary by series — use the machine's own parameter manual.*

## 1. Offsets
- **Work offsets** (OFFSET › WORK): `G54–G59`, extended `G54.1 P1–P48` (or more with
  option). The **EXT/00** offset shifts every work offset — handy for a global shift,
  dangerous if forgotten. Check it's zero (or intended) at every setup.
- **Tool length** (`G43 H_`): geometry = measured length; **wear** = small adjustments
  made in production to hold size. Never adjust geometry to hold size — wear offsets
  keep the "measured" value honest and can be reset on tool change.
- On lathes (T-series): `T0101` = tool 1, offset 1; X wear values are on *diameter*
  (if diameter programming is set) — moving X wear by 0.02 changes the diameter by 0.02.
- **Cutter radius comp** (`G41/G42 D_`): the D offset holds radius (or wear) — check
  whether your programs use full radius (CAM in "computer" comp) or wear-only ("wear"
  or "reverse wear" comp). Mixing these scraps parts.

## 2. MDI and handle
- MDI to call tools and position: `G91 G28 Z0;` sends Z home (incremental zero — not
  "go to zero"). `G90` absolute is the default you want back afterwards.
- Handwheel at ×100 near parts, ×10/×1 in the last millimetre; never rapid-jog toward
  a part with the table loaded.

## 3. Macro B essentials
- **Local** `#1–#33` (arguments, cleared per call), **common** `#100–#199` (cleared on
  reset/power-off on most setups) and `#500–#999` (retained), **system** `#1000+`
  (offsets, positions, alarms).
- Call with `G65 P9010 A1. B2.` (args A→#1, B→#2, …). Use subprogram numbers in the
  O9000s only if you know they may be edit-protected by parameter.
- Production uses: part counters (`#500=#500+1`), conditional tool life (`IF [#501 GE
  500] GOTO 900`), raise a custom alarm with `#3000=1 (TOOL LIFE REACHED)`, and
  probing logic that writes offsets into the system variables.
- System variable numbers for offsets differ by series and offset memory type — look
  them up; writing the wrong one silently changes another tool's offset.
- Trap empty variables: `#0` is null, not zero; test `IF [#1 EQ #0]`.

## 4. Alarms: recovery pattern
1. **Read the full alarm** number and text (MESSAGE / ALARM screen and history).
2. **Overtravel (OT0500/0501 etc.):** jog the axis back in the opposite direction
   (often needs holding the overtravel release on some machines), then reset.
3. **PS alarms** (program errors, e.g. bad G-code combination): fix the program; reset
   clears it. Know which line — check the program position before reset.
4. **Servo/spindle alarms** (SV/SP): note them with the diagnostic data before resetting;
   repeated alarms = mechanical or drive fault, not something to reset through.
5. **Reference return required** after battery/encoder issues — re-home only as the
   machine manual says; absolute encoder batteries must be changed with power **on**.
6. Restart mid-program with care: use program restart/`N` search with modal states
   (tool, offset, spindle, coolant, `G43`) re-established.

## 5. Parameters
- Need **PWE=1** (Parameter Write Enable) in the SETTING screen, which raises alarm 100
  until set back to 0. Write down the old value first.
- Back up parameters, offsets, macros and programs to memory card/USB/ethernet before
  any change; keep a dated copy off the machine.

## Gotchas
- Leaving `EXT` offset or a single-block/dry-run/optional-stop setting on after a job.
- `#100` series values vanishing on reset when the macro assumes they persisted.
- Typing wear into geometry by being on the wrong offset page.

## Verify
- [ ] EXT offset checked; all work offsets match the setup sheet.
- [ ] Size adjustments made in wear, not geometry.
- [ ] Macros test for null arguments and alarm with readable text.
- [ ] Parameter changes logged with old/new values; PWE back to 0.
- [ ] Recent full backup stored off the machine.
