---
id: engineering-technology.electronics-engineering.pcb-design.stackup-and-placement
name: stackup-and-placement
category: engineering-technology
field: electronics-engineering
product: pcb-design
tags: [pcb-design, pcb-layout, stack-up, stackup, layer-stack, 4-layer-pcb, 6-layer-pcb, ground-plane, return-path, placement, floorplanning, controlled-impedance, microstrip, trace-width, ipc-2221, ipc-2152, ipc-7351, dfm, design-for-manufacturing, fiducials, kicad, altium-designer]
level: practitioner
status: draft
description: "Choose a PCB stack-up and place parts so routing, power and return paths work: 4/6-layer stacks, solid reference planes, placement order, DFM rules of thumb."
sources:
  - "Ott, Electromagnetic Compatibility Engineering"
  - "Johnson & Graham, High-Speed Digital Design: A Handbook of Black Magic"
  - "IPC-2221, Generic Standard on Printed Board Design"
  - "IPC-2152, Standard for Determining Current Carrying Capacity in Printed Board Design"
  - "Bogatin, Signal and Power Integrity — Simplified"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# PCB stack-up and placement — most layout quality is decided before routing

**Goal:** pick a layer stack and a component placement that give every signal a
continuous, nearby return path and every power rail a short, low-inductance route,
so routing becomes mechanical rather than heroic.

## 1. Choose the stack-up
Rule: **every signal layer sits directly next to a solid reference plane**, and
fast signals never change reference without a nearby return via.

| Layers | Recommended stack | Notes |
|---|---|---|
| 2 | SIG+pour / GND-dominant | Keep bottom as unbroken GND as far as possible; only short jumpers on it. Fine for slow/low-density work. |
| 4 | SIG / GND / PWR / SIG | The workhorse. Ask for a thin L1–L2 prepreg (~0.1–0.2 mm) so top signals couple tightly to GND. Alternative SIG / GND / GND / SIG with power routed as pours on the outer layers is often better for EMC. |
| 6 | SIG / GND / SIG / PWR / GND / SIG | Inner SIG on L3 should be closer to L2 than to L4. Route the fastest nets on L1 or L3 referenced to GND. |

- Get the fab's **standard stack-up** (thicknesses, laminate, εr) before computing
  impedances; designing to a stack they don't stock costs time and money.
- **50 Ω microstrip on FR-4**: width ≈ 1.8–2× the dielectric height to the plane
  (0.2 mm prepreg → roughly 0.35–0.38 mm). Always confirm with a field solver
  (KiCad's calculator, Saturn PCB Toolkit, or the fab's own) and order controlled
  impedance with ±10 % tolerance when it matters.
- Keep the stack **symmetric** (copper and dielectric) to avoid warp.

## 2. Placement order
1. **Fixed mechanics**: board outline, mounting holes, connectors, switches, LEDs,
   heat sinks, keep-outs (from the enclosure CAD, as a DXF/STEP).
2. **Critical-path parts**: switching regulators (hot loop: input cap, switch, diode/
   sync FET as tight as possible), crystals (≤ 5–10 mm from the pin, no traces under
   them), high-speed ICs and their connectors so the fast nets are short and direct.
3. **Main ICs, oriented for routing**: rotate so pin escape flows toward the
   connected part. Use the ratsnest; minimise crossings.
4. **Decoupling** on the same side as the IC pins where possible, smallest value
   closest, via to plane right at the cap pad.
5. **Everything else**: pull-ups, LEDs, test points.

Partition by function (power, analog, digital, RF, I/O) **in placement**, with one
continuous ground plane. Do not split the ground plane to "separate" analog and
digital unless you can name the current you are steering; a split under a trace
destroys its return path.

## 3. Routing discipline that placement must enable
- Signals on L1/L4 of a 4-layer board must not cross gaps in L2/L3. Put a stitching
  via (GND-to-GND) within a few mm of every layer change of a fast signal.
- Trace width for current (IPC-2221 external, 1 oz, 10 °C rise): ~0.3 mm per 1 A;
  internal layers need roughly 2.5× the width. IPC-2152 is the newer, more realistic
  method — use a calculator based on it for anything over a few amps.
- Default clearances: for low voltage, fab minimum + margin (0.15–0.2 mm). For mains
  or > 50 V, use the safety standard's creepage/clearance (e.g. IEC 62368-1), not
  IPC-2221 spacing tables.

## 4. DFM checklist
- Footprints to IPC-7351 nominal density unless space forces least-material.
- Small passives (0402 and below): symmetric copper on both pads (thermal reliefs
  or equal trace widths) to prevent tombstoning.
- **Fiducials**: 3 global per board/panel, 1 mm copper dot with ~2–3 mm mask opening;
  local fiducials near fine-pitch BGAs if the assembler asks.
- Via-in-pad only filled and capped (costs extra); otherwise dog-bone.
- Keep parts ≥ 3–5 mm from V-score/break-away edges; tall parts away from edges
  that get handled.
- Test points on every rail, reset, and key bus, reachable from one side.

## Verify
- [ ] Every signal layer is adjacent to a solid plane; the stack matches a fab-standard build.
- [ ] Controlled-impedance widths come from a field solver using the fab's εr and thicknesses.
- [ ] No fast trace crosses a plane split or void (check plane layers with signal overlay).
- [ ] Switching regulator hot loops and crystals are placed first and are compact.
- [ ] Every IC power pin has a decoupling cap within a few mm with its own via.
- [ ] Fiducials, test points and edge clearances meet the assembler's requirements.
