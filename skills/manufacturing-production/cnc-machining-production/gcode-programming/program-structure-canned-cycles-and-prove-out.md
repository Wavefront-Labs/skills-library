---
id: manufacturing-production.cnc-machining-production.gcode-programming.program-structure-canned-cycles-and-prove-out
name: program-structure-canned-cycles-and-prove-out
category: manufacturing-production
field: cnc-machining-production
product: gcode-programming
tags: [gcode-programming, g-code, gcode, nc-program, iso-6983, cnc-programming, manual-programming, safe-start-line, modal-codes, g90, g91, g17, g43, g54, g80, canned-cycles, g81, g83, g84, g73, g76, g71, rigid-tapping, peck-drilling, subprogram, m98, m99, cutter-compensation, g41, g42, lead-in, prove-out, single-block, dry-run, feed-override, distance-to-go, cnc-machining-production]
level: practitioner
status: draft
description: "Hand-write G-code that is safe to restart: safe start lines, per-tool blocks, canned drilling and tapping cycles, subprograms, cutter comp lead-ins, and first-part prove-out."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Program structure, canned cycles and prove-out

**Goal:** G-code that any setter can read, restart at any tool, and prove out on the
first part without a crash — on FANUC-style controls (most of the principles carry
to Haas, Siemens ISO mode, Mazak EIA, etc.).

*Draft: examples are FANUC/Haas-style milling syntax. Canned cycle parameters
(especially G83 Q, G84 and lathe G71/G76) differ between controls and parameter
settings — check the control manual before using.*

## 1. Program skeleton
```
%
O1001 (PART 123-A OP1 REV C)
(T1 D50 FACE MILL / T2 D10 3FL ENDMILL / T3 D8.5 DRILL / T4 M10x1.5 TAP)
G21 G17 G40 G49 G80 G90 G94      (safe start: metric, XY plane, cancel comps/cycles)
N10 (FACE)
T1 M6
G54 G90 G0 X-35. Y0 S2000 M3
G43 H1 Z50. M8
...
G0 Z50. M9
G91 G28 Z0. M5
G90
M1                                (optional stop between tools)
N20 (ROUGH POCKET)
T2 M6
...
M30
%
```
- **Every tool block is self-contained:** tool, work offset, absolute mode, spindle,
  `G43 H` with the matching H, coolant. Then restarting at `N20` works without
  running from the top.
- Keep the **safe start line** at the top *and* the modal resets that matter at each
  N-block (some controls carry `G41`, `G91`, `G81` across tool changes otherwise).
- Comments name the operation and tool; the header lists all tools.

## 2. Canned cycles (milling)
- `G81` drill/spot: `G98 G81 Z-5. R2. F150` then positions `X10. Y10.` `X20.`…; `G80`
  to cancel. **G98** returns to the initial Z between holes (clears clamps), **G99** to
  the R plane (faster, only when nothing's in the way).
- `G83` peck (full retract) / `G73` chip-break (short retract): `Q` = peck depth per
  pass. Deep holes in sticky materials: full retract.
- `G84` rigid tap: feed must equal **pitch × rpm** (in feed/min mode) or use
  feed-per-rev. M10×1.5 at 500 rpm → F750 (mm/min). Many controls need `M29 S500`
  before G84 for rigid tapping — control-dependent.
- Always `G80` before a tool change or a rapid move to a new area.

## 3. Subprograms
- Repeat geometry at several locations: main program positions, `M98 P2001` calls the
  feature in `G91` or relative to a local offset (`G52`), `M99` returns.
- Return to `G90` explicitly after an incremental subprogram — a forgotten `G91` is a
  classic crash.

## 4. Cutter compensation
- `G41` (climb, left) / `G42` with a `D` register. Apply comp on a **linear lead-in move
  longer than the tool radius**, perpendicular-ish to the first wall, away from the part;
  cancel (`G40`) on a lead-out move clear of the part.
- Interference alarms on inside corners smaller than the tool radius = geometry problem,
  not a control problem.

## 5. Prove-out of the first part
1. **Graphics / simulation** at the control or in a verifier.
2. Check offsets: work offset values, tool lengths (H) and radii (D) against the setup sheet.
3. **Dry run above the part** (work offset Z raised, or the control's Z-lock/dry run) if
   the setup allows — watch the path.
4. First real run: **single block**, **rapid override 25%**, **feed override low**, hand on
   feed hold. On the approach to the part, watch **distance-to-go**: if it's more than
   the visible gap, stop.
5. Measure after critical features; adjust wear offsets, not the program.
6. Once proven, mark the program "proven" with date; changes after that need a re-prove.

## Gotchas
- Decimal points: on many FANUC settings `X10` = 0.010 mm (least input increment), `X10.`
  = 10 mm. Always write the point.
- `G28` goes *via* the point you give: `G91 G28 Z0` is safe; `G90 G28 Z0` drives to work Z0 first.
- `H` number not matching the tool → Z off by a whole tool length.
- Modal `G01` left on, then a "rapid" line without `G0` moves at feed — or the opposite.

## Verify
- [ ] Every tool block can be restarted alone.
- [ ] Every number that should have a decimal point has one.
- [ ] Each canned cycle cancelled with G80; incremental subprograms return to G90.
- [ ] First part run single-block with reduced overrides and distance-to-go checked.
- [ ] Proven program saved with revision and date.
