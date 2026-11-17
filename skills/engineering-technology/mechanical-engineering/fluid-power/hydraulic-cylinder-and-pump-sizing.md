---
id: engineering-technology.mechanical-engineering.fluid-power.hydraulic-cylinder-and-pump-sizing
name: hydraulic-cylinder-and-pump-sizing
category: engineering-technology
field: mechanical-engineering
product: fluid-power
tags: [hydraulics, fluid-power, hydraulic-cylinder, cylinder-sizing, pump-sizing, hydraulic-pump, electric-motor-sizing, rod-buckling, euler-buckling, regenerative-circuit, pressure-intensification, counterbalance-valve, relief-valve, pipe-sizing, hose-sizing, flow-velocity, iso-4406, contamination, reservoir, heat-load, pneumatics, hydraulic-circuit]
level: practitioner
status: verified
description: "Size a hydraulic cylinder, pump, motor and lines: force and speed from area, rod buckling, regen and intensification traps, pipe velocities, power and heat."
sources: ["Esposito, Fluid Power with Applications (Pearson)", "Parker Hannifin, Industrial Hydraulics Technology (training manual)", "ISO 4406 Hydraulic fluid power — Fluids — Method for coding the level of contamination by solid particles", "ISO 1219-1 Fluid power systems and components — Graphical symbols"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Hydraulic cylinder and pump sizing — from load to power unit

**Goal:** choose bore, rod, pump flow, motor power and line sizes for a linear actuator so
it meets force and speed at a sensible working pressure, does not buckle, stall or run
away, and does not overheat.

## 1. Requirements table
Load force at each phase (extend, hold, retract), stroke, speeds, cycle time, mounting
style, duty cycle and ambient. Include friction, acceleration (`F = m a`) and
gravity components — peak force is often during acceleration, not the static load.

## 2. Cylinder bore
`A_bore = F / (p_avail * eta_cyl)`. Design so the **load needs about 70–80 % of system
pressure** at the cylinder, leaving margin for valve and line losses (several bar each).
With p_avail = 160 bar at the cylinder and F = 80 kN: A = 80 000 / (16 MPa x 0.95) =
5263 mm2 -> d = 82 mm (computed: 5263 mm2, 81.9 mm) -> choose standard 100 mm bore (ISO 3320 metric bore series: 63, 80, 100, 125... (gated: unconfirmed, source is paywalled or blocked)).

Annulus area for retract: `A_ann = pi/4 (D^2 - d_rod^2)`. Area ratio
`phi = A_bore / A_ann` (often ~1.25–2 (gated: unconfirmed, source is paywalled or blocked)).

## 3. Rod buckling
Treat the rod as a column at full extension: Euler `F_cr = pi^2 E I / (K L)^2`, with
effective length factor K from mounting (pin-pin 1.0, fixed-free 2.0 — the worst; check
the manufacturer's stroke-factor table, which accounts for mount style). Apply a safety
factor of roughly 3–4 on Euler for hydraulic cylinders (gated: unconfirmed, source is paywalled or blocked). Long strokes push you to a
bigger rod or a stop tube, not a bigger bore.

## 4. Flow and pump
- Extend flow: `Q = A_bore x v` (L/min = mm2 x m/s x 0.06). Retract needs less flow
  for the same speed, but returns `phi x Q` from the cap side — size the return
  line and valve for this.
- Pump displacement: `Vg = Q / (n x eta_vol)`; volumetric efficiency ~0.90–0.95 for gear
  pumps, higher for piston pumps (gated: unconfirmed, source is paywalled or blocked).
- Drive power: `P [kW] = p [bar] x Q [L/min] / (600 x eta_total)`, eta_total ~0.80–0.85 (gated: unconfirmed, source is paywalled or blocked).
  Example: 180 bar (pump, 160 bar at the cylinder plus losses) x 60 L/min / (600 x 0.85) = 21.2 kW (computed). Unit check: 1 mm2 x 1 m/s = 0.06 L/min.
- High flow for a short part of the cycle: consider an accumulator or a variable pump
  instead of a big fixed pump (the excess flow over relief is pure heat).

## 5. Lines
Recommended mean velocities (common practice; manufacturer tables vary slightly):
suction 0.6–1.2 m/s, return 2–4 m/s, pressure 3–6 m/s (gated: unconfirmed, source is paywalled or blocked). `d = sqrt(4 Q / (pi v))`.
A cramped suction line causes pump cavitation and noise — keep it short, large and with
positive head where possible.

## 6. Circuit traps
- **Pressure intensification**: with meter-out speed control on extend, the rod side can
  see `p_supply x phi` (plus load effects). A 2:1 cylinder at 200 bar can see ~400 bar
  in the annulus (arithmetic: p x phi). Check rod-side seal and hose ratings.
- **Over-running (gravity) loads** need a counterbalance or load-holding valve, set
  ~1.3x the load-induced pressure (gated: unconfirmed, source is paywalled or blocked); check valves alone let a vertical load creep through
  spool leakage.
- **Regenerative extend** connects rod-side flow to the cap side: faster extend
  (`v = Q / A_rod`) but force only `p x A_rod`.
- Relief valve set about 10 % above max working pressure (gated: unconfirmed, source is paywalled or blocked) (and at or below component
  ratings).
- Cushioning at stroke ends when speed exceeds ~0.1 m/s with significant mass (gated: unconfirmed, source is paywalled or blocked).

## 7. Heat, reservoir, cleanliness
Lost power (relief flow, throttling, pump/motor inefficiency) becomes heat. Estimate it
per cycle; if natural reservoir dissipation is insufficient, add a cooler. A traditional
industrial reservoir sizing rule is 3x pump flow per minute (gated: unconfirmed, source is paywalled or blocked) (mobile systems use much
less with coolers). Specify cleanliness to the most sensitive component, e.g. ISO 4406
around 17/15/12 for proportional/servo valves versus ~19/17/14 for basic gear-pump
circuits (gated: unconfirmed, source is paywalled or blocked) — confirm against component manufacturer requirements.

## Verify
- [ ] Load can be moved at ~70–80 % of available pressure, including acceleration.
- [ ] Rod buckling safety factor >= ~3 at full stroke with the actual mounting.
- [ ] Rod-side pressure (intensification) within component ratings.
- [ ] Line velocities within the recommended bands; return line sized for phi x Q.
- [ ] Motor power and heat balance computed over the duty cycle; oil temperature
      stays below ~60 C (gated: unconfirmed, source is paywalled or blocked) (or the fluid supplier's limit).
