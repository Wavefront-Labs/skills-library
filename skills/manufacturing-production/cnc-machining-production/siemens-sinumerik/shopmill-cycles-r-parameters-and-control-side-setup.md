---
id: manufacturing-production.cnc-machining-production.siemens-sinumerik.shopmill-cycles-r-parameters-and-control-side-setup
name: shopmill-cycles-r-parameters-and-control-side-setup
category: manufacturing-production
field: cnc-machining-production
product: siemens-sinumerik
tags: [siemens-sinumerik, sinumerik, sinumerik-828d, sinumerik-840d-sl, sinumerik-one, sinumerik-operate, shopmill, shopturn, programguide, conversational-programming, g-code, cycles, cycle81, cycle83, cycle800, pocket4, r-parameters, gud, user-variables, frames, g54, trans, atrans, rot, tool-management, cutting-edge, d-number, tool-list, measure-workpiece, measure-tool, setup, cnc-machining-production]
level: practitioner
status: draft
description: "Run and program SINUMERIK controls: ShopMill/ShopTurn step programs vs G-code with cycles, R-parameters and frames (TRANS/ROT), tool and edge data, and setting work offsets at the control."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ShopMill, cycles, R-parameters and control-side setup on SINUMERIK

**Goal:** set up and program a SINUMERIK 828D/840D sl/ONE machine with SINUMERIK
Operate, choosing correctly between conversational (ShopMill/ShopTurn) and G-code,
and using frames and parameters so programs adapt instead of being rewritten.

*Draft: from SINUMERIK Operate 4.x-era practice. Machine builders configure screens,
measuring cycles and tool management differently; options (e.g. CYCLE800 swivel,
measuring) must be licensed.*

## 1. Which programming mode?
- **ShopMill (milling) / ShopTurn (turning):** step-based "work plan" with graphic
  dialogs (contour, pocket, drill pattern). Great for one-offs and simple repeat parts
  at the machine; readable by setters. Each step stores tool, feeds and geometry.
- **programGUIDE G-code:** standard ISO-style G-code with Siemens cycles called from
  dialog screens (they insert `CYCLE81(...)`, `CYCLE83(...)`, `POCKET4(...)` lines).
  Best for CAM output and complex logic.
- Mixed: CAM posts can output G-code with Siemens cycles; ShopMill programs can contain
  G-code blocks. Don't convert between them by hand.

## 2. Cycles you'll use constantly
- Drilling: `CYCLE81` (drill), `CYCLE82` (dwell), `CYCLE83` (deep hole/peck),
  `CYCLE84` (rigid tap), `CYCLE86` (bore).
- Milling: `POCKET3/POCKET4` (rect/circular), `CYCLE61` (face), contour pocketing.
- `CYCLE800` (swivel plane) for 3+2 machining on 5-axis/swivel-head machines — needs
  the kinematics data set up by the builder; wrong swivel data record = wrong angle.
- Parameter order in cycle calls changes between software versions; edit through the
  dialog screen (the "recompile" function) rather than by typing the call.

## 3. R-parameters and variables
- `R0–R99` (or more, set by machine data) are global arithmetic parameters:
  `R1=25.4  G1 X=R1*2 F=R2`. Note the `=` needed when an axis takes an expression.
- **User variables (GUD/LUD)** with names: `DEF REAL PARTCOUNT` — readable and typed.
- Control flow: `IF R1>10 GOTOF LABEL1`, `FOR`/`WHILE` loops, `REPEAT LABEL P=3`.
- Raise a message for the operator: `MSG("Check insert")` and stop with `M0`.

## 4. Frames (where SINUMERIK shines)
- **Settable work offsets** `G54–G57`, `G505–G599`.
- **Programmable frames** layer on top: `TRANS X10` (shift, replaces previous),
  `ATRANS X10` (additive), `ROT Z30`, `AROT`, `MIRROR X0`, `SCALE`.
- Pattern of identical features: one subprogram, called after `ATRANS` for each
  position. Reset frames with a bare `TRANS` or at program end — a frame left active
  will move the next program.

## 5. Tool management and setup
- Tools have a name/number, cutting edges `D1…D9` each with length and radius plus
  **wear** values. Use wear to hold size; geometry stays as measured.
- With tool management active, tools are called by **name** (`T="DRILL_8.5"`) and the
  control picks a sister tool when life runs out — set tool life/counts.
- **Measure workpiece** (in JOG › Meas. workpiece) with a probe or by touching edges:
  choose the target offset (e.g. G54) and press *Set work offset*. Check which
  offset is active before cutting.
- **Measure tool** on a tool setter or by scratching against a known surface.

## Gotchas
- Inch/metric (`G70/G71`, `G700/G710`) and diameter/radius programming (`DIAMON`) on
  lathes — confirm the modal state at program start.
- Basic frames and "total offsets" can include system frames (from measuring);
  the active work offset screen shows the sum — check it, not just G54.
- ShopMill programs saved on a control with a newer Operate version may not open on older ones.

## Verify
- [ ] Program mode chosen deliberately; CAM output uses the correct Siemens post.
- [ ] Active work offset and total frame checked on the screen before first cut.
- [ ] Programmable frames reset at program end.
- [ ] Size held with wear values; tool life set where tool management is used.
- [ ] Simulation/simultaneous recording run before the first part.
