---
id: engineering-technology.automotive-vehicle-engineering.nvh.mirror-and-a-pillar-flow-noise
name: mirror-and-a-pillar-flow-noise
category: engineering-technology
field: automotive-vehicle-engineering
product: nvh
tags: [aeroacoustics, wind-noise, a-pillar-vortex, mirror-noise, side-glass, aeroacoustic-wind-tunnel, microphone-array, lattice-boltzmann, les, flow-noise, dipole-noise]
level: practitioner
status: gated
description: "Reduce mirror and A-pillar flow noise: vortex and separation sources, transmission through glass, tunnel and CFD methods, and shape and sealing countermeasures."
sources:
  - "Harrison, Vehicle Refinement (chapter list)"
  - "Aeroacoustics sections in vehicle refinement references; Zwicker and Fastl, Psychoacoustics (chapter list)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Mirror and A-pillar flow noise

## 1. Sources
- **Separated flow and vortex shedding** from the mirror housing and the A-pillar (A-pillar vortex) produce pressure fluctuations on the side glass. These hydrodynamic fluctuations and the acoustic radiation (dipole sources on surfaces) excite the glass, which radiates into the cabin.
- **Reattachment** on the side window and mirror wake impinging on the glass or door seal.
- **Gaps and steps** around mirror base, wipers, door frame; **tonal** sources from cavities, grooves or rough trim.
Rule of thumb often cited (Curle dipole scaling): dipole noise scales with flow speed to roughly the sixth power, so speed matters a lot (gated: unconfirmed, source is paywalled or blocked); confirm by measurement. Frequency content is broadband with low-frequency dominated hydrodynamic pressure.

## 2. Path
Pressure fluctuations act on the side glass and A-pillar seals; transmission depends on glass thickness and laminate (acoustic laminated glass improves coincidence-frequency transmission loss), door seals, and body panel. Hydrodynamic pressure transmits well at low frequency (see body acoustics).

## 3. Measurement
- **Aeroacoustic wind tunnel:** low background noise, microphone array near the vehicle and head-position microphones (artificial head) inside; surface pressure microphones on the side glass.
- **Road tests** at constant speed with the same microphones and consistent wind conditions.
- **Source ranking** with covering and tape-off tests, beamforming and acoustic cameras.
- **Subjective evaluation** with loudness and articulation index metrics (see psychoacoustic metrics).

## 4. Simulation
Transient CFD with scale-resolving methods (large-eddy or detached-eddy simulation, or lattice-Boltzmann solvers) provides surface pressure fluctuations for use in structural-acoustic models (SEA or FE) to predict cabin noise. Cost is high, and validation against tunnel data on a simplified shape is needed.

## 5. Countermeasures
Mirror shape (smooth housing, rounded edges, base cut-outs), mirror position away from the glass and with the flow, A-pillar radius and gutter design, wiper park position, A-pillar trim and seal flushness, glass thickness or laminate, extra damping, reducing steps in door frame, and carefully shaped drip rails.

## Verify
- [ ] Source ranked by tape-off or array before design changes.
- [ ] Interior metrics (A-weighted level, loudness, articulation index) improved at speed and yaw.
- [ ] CFD or SEA model validated against tunnel data.
- [ ] Side glass and seal path also checked.
