---
id: engineering-technology.automotive-vehicle-engineering.nvh.nvh-target-cascade
name: nvh-target-cascade
category: engineering-technology
field: automotive-vehicle-engineering
product: nvh
tags: [nvh-targets, target-cascade, vehicle-nvh-targets, benchmarking, ntf-target, mount-stiffness-target, interior-spl, articulation-index, loudness-target, target-setting]
level: practitioner
status: draft
description: "Set an NVH target cascade: vehicle-level interior sound goals, system and component targets via transfer functions, benchmarking, margins and gate sign-off."
sources:
  - "Harrison, Vehicle Refinement (chapter list)"
  - "Zwicker and Fastl, Psychoacoustics (chapter list)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# NVH target cascade

## 1. Purpose
Turn a customer-level goal (a quiet, refined car with a recognisable sound) into engineering targets for systems and parts, so each team knows what to deliver and the whole adds up.

## 2. Levels
1. **Vehicle level:** interior sound pressure level (overall and in bands, dB(A)) at standard conditions (idle, 50/80/100/120 km/h cruise, full-throttle acceleration, rough road), loudness (sone), articulation index/speech intelligibility, sharpness, roughness, tonality limits, vibration at steering wheel, seat rail and floor.
2. **System level:** body noise transfer functions (NTF in dB re 1 Pa/N), vibration transfer functions (VTF), body stiffness and modes (see body stiffness skills), sound package insertion loss, wind noise (see seal and aero skills), and tyre-road excitation.
3. **Component level:** engine and motor forces at order levels, mount dynamic stiffness and isolation, exhaust and intake sound power, bush rates (see bush NVH tuning), subframe stiffness, damper and tyre force transmissibility.

## 3. Setting vehicle targets
- Benchmark: measure competitor vehicles with the same procedure and microphones, plot level and metrics vs speed or rpm.
- Choose positioning for the brand and segment (a point on the distribution of benchmarks), and subjective ratings through jury testing (see sound quality jury testing).
- Regulatory limits for exterior noise (pass-by test) are separate; interior targets are commercial.

## 4. Cascade by transfer path
Interior pressure p = sum over paths of F_i x NTF_i (source force times transfer function), a complex (magnitude and phase) sum, not a sum of dB levels; so for a target p_target at the ear, with a share of the budget to each path, derive allowed forces or required NTFs. TPA on a benchmark or predecessor provides the path breakdown (see classical TPA and path contribution ranking). If paths are incoherent and equal, N paths each need to be 10 log10(N) dB below the target (3.0 dB for 2, 6.0 dB for 4; computed). Add margins for unit and build variation (several dB) and for items still unknown.

## 5. Governance
Table with columns: requirement, level, metric, test method, benchmark, target, owner, current status (CAE, prototype test), risk. Review at design gates; update when the product changes. Targets must have a defined test method (operating condition, microphone, filter) or they are unverifiable.

## 6. EV-specific
Without engine masking, other sounds (motor whine, inverter tones, HVAC, tyre, wind) come to the fore; add tonal and psychoacoustic targets and the AVAS exterior requirements (see EV NVH skills).

## Verify
- [ ] Every target has a metric, condition and measurement method.
- [ ] Path-based cascade sums to the vehicle target with margin.
- [ ] Benchmarks measured with the same method.
- [ ] Status tracked from CAE through prototype test.
