---
id: engineering-technology.automotive-vehicle-engineering.nvh.suspension-bush-nvh-tuning
name: suspension-bush-nvh-tuning
category: engineering-technology
field: automotive-vehicle-engineering
product: nvh
tags: [bush-nvh-tuning, bushing, hydro-bush, dynamic-stiffness, loss-angle, road-noise, ride-harshness, wheel-hop, decoupling, suspension-nvh, bush-tuning]
level: practitioner
status: gated
description: "Tune suspension bushes for NVH: dynamic versus static stiffness, loss angle, hydro-bush damping, decoupling, and the ride, handling and noise trade-offs, verified by TPA."
sources:
  - "Harrison, Vehicle Refinement (chapter list)"
  - "Reimpell, Stoll and Betzler, The Automotive Chassis (chapter list)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Suspension bush NVH tuning

## 1. What the bush does
Rubber or hydraulic bushes sit between suspension links and the body or subframe. They decouple road-induced vibration from the body (low dynamic stiffness at noise frequencies) while controlling wheel motion for ride and handling (higher static or low-frequency stiffness).

## 2. Properties that matter
- **Static rate** (N/mm) in radial, axial, conical and torsional directions for kinematics and compliance.
- **Dynamic stiffness** vs frequency (typically measured 5-500 Hz): elastomers stiffen with frequency and amplitude; the dynamic-to-static ratio is often 1.2 to 2 or more depending on compound (gated: unconfirmed, source is paywalled or blocked).
- **Loss angle** (damping, tan delta): higher damping helps wheel-hop control (roughly 10-15 Hz; 11 Hz computed for a 200 kN/m tyre rate and 40 kg unsprung mass) and shake but usually raises high-frequency transmissibility.
- **Amplitude dependence** (Payne effect: in filled rubber the storage modulus falls as strain amplitude rises): small road vibrations see higher stiffness than large ones; test at representative amplitudes.
- **Temperature dependence:** stiffness and damping change strongly with temperature and ageing.

## 3. Tuning workflow
1. Identify the dominant paths with transfer path analysis (see structure-borne road noise and classical TPA): which bush axes contribute most at the problem frequencies.
2. For those axes, ask whether lowering dynamic stiffness is possible without hurting compliance steer or handling (see compliance steer).
3. Use directional design: soft in the axis of noise transmission (often the longitudinal direction at the lower control arm) and stiff in the axis that governs toe and camber.
4. Use hydro-bushes (fluid-filled with a decoupler) to get high damping at low frequency (ride and wheel-hop) and low dynamic stiffness at higher frequency.
5. Consider bush voids, shaped inner sleeves, and metal-rubber stops to tailor nonlinearity.
6. Re-measure NTF and road noise after changing; adjust subframe mounts too (see subframe mount design).

## 4. Trade-offs
Softer bushes reduce harshness and noise but increase compliance steer and reduce steering response and braking stability; control through geometry (for example toe-control links) rather than stiffness alone.

## 5. Specification
Spec static rates with a tolerance, dynamic stiffness at defined frequencies and amplitudes, loss angle range, durability (cycle test), and ageing. Record the test method so supplier and OEM measure the same.

## Verify
- [ ] Dynamic stiffness and loss angle measured at relevant amplitude and temperature.
- [ ] Priority bush axes chosen from TPA ranking.
- [ ] Ride, compliance and handling re-checked after the change.
- [ ] Supplier test method and tolerances documented.
