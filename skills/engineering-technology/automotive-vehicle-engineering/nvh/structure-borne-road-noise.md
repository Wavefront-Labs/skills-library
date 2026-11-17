---
id: engineering-technology.automotive-vehicle-engineering.nvh.structure-borne-road-noise
name: structure-borne-road-noise
category: engineering-technology
field: automotive-vehicle-engineering
product: nvh
tags: [structure-borne-noise, road-noise, roar, spindle-forces, subframe-isolation, noise-transfer-function]
level: practitioner
status: gated
description: "Diagnose and control structure-borne road noise (roar, 20-400 Hz): spindle force input, bush and subframe paths, NTF targets and body panel participation."
sources:
  - "Harrison, Vehicle Refinement"
  - "Genuit, Sound-Engineering im Automobilbereich"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Structure-borne road noise

1. Mechanism: road texture excites the tyre; forces at the spindle go through suspension links, bushings and the subframe into the body, then radiate as interior sound; dominated by 50-300 Hz (road roar often 100-250 Hz (gated: unconfirmed, source is paywalled or blocked)).
2. Measure: wheel force transducers or accelerometers at spindle in operational driving on standard rough surfaces; interior sound and floor/seat-rail acceleration; run at constant speeds 50-100 km/h (a typical choice, not a standard).
3. Transfer functions: noise transfer function (NTF in Pa/N) from each body interface force to the driver's ear; targets by frequency band set from benchmarks.
4. Controls: tyre selection and tyre-cavity damping (see tyre cavity resonance), spindle force reduction by stiffer or softer bushes in the dominant path directions, decoupled subframe with tuned mounts, body-side stiffness at attachment points, panel damping, local absorbers.
5. Target setting: allocate dB from vehicle-level target to force and NTF targets at each path.
6. Tools: TPA, CAE with FE-based NTF and tyre input forces; verify with prototype tests.
7. Cost/mass trade-offs: damping and mass dampers versus design changes upstream.

**Gotchas:** surface choice and tyre wear change levels; keep a standard surface and tyres.

## Verify
- [ ] NTF measured at key interfaces meets targets.
- [ ] Interior noise at 80 km/h on the standard surface within the programme target.
