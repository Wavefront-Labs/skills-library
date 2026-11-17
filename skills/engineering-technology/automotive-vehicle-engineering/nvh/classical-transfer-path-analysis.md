---
id: engineering-technology.automotive-vehicle-engineering.nvh.classical-transfer-path-analysis
name: classical-transfer-path-analysis
category: engineering-technology
field: automotive-vehicle-engineering
product: nvh
tags: [classical-tpa, tpa, transfer-path-analysis, mount-stiffness, noise-transfer-function, force-identification]
level: practitioner
status: gated
description: "Run classical TPA: measure mount dynamic stiffness and body-side transfer functions, compute path forces and contributions, and check against the total response."
sources:
  - "Harrison, Vehicle Refinement"
  - "Plunt, Examples of Using Transfer Path Analysis (TPA) together with CAE-Models to Diagnose and Find Solutions for NVH Problems Late in the Vehicle Development Process, SAE Technical Paper 2005-01-2508, doi:10.4271/2005-01-2508"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Classical TPA

1. Define paths: each mount, link and acoustic path into the cabin, three directions at each interface (typically 30-60 paths (gated: unconfirmed, source is paywalled or blocked)).
2. Operational data: run the vehicle (e.g. rpm sweep, road) and measure accelerations on both sides of each mount (active and passive side) and the target response (interior sound/ seat-rail vibration).
3. Mount stiffness: measure dynamic stiffness `k(f)` of each mount on a rig; or use its manufacturer data; force = `k(f) * (x_active - x_passive)`.
4. Transfer functions: measure body-side FRFs from force to target (NTF in Pa/N or vibration/N) using an impact hammer or shaker at the passive-side points in all directions; reciprocal methods put a volume-source or loudspeaker in the cabin.
5. Contributions: `p_i = H_i * F_i`, sum vector-wise `p_total = sum p_i`, compare with the measured response (validity check: within about 3 dB over the range, a common criterion (gated: unconfirmed, source is paywalled or blocked)).
6. Rank by magnitude over frequency/order; identify the dominant path(s) and check phases for cancellation.
7. Condition: the mount dynamic stiffness should be much lower than the body-side impedance for the approach to hold.

**Gotchas:** wrong directions, missed paths and poor mount stiffness data yield poor sum agreement.

## Verify
- [ ] Synthesised sum matches the measured response within the stated tolerance.
- [ ] Top 3 paths identified and quantified in dB.
