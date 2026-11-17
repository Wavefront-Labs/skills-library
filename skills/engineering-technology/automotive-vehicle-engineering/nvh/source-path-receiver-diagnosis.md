---
id: engineering-technology.automotive-vehicle-engineering.nvh.source-path-receiver-diagnosis
name: source-path-receiver-diagnosis
category: engineering-technology
field: automotive-vehicle-engineering
product: nvh
tags: [nvh, noise-vibration-harshness, source-path-receiver, order-tracking, order-analysis, campbell-diagram, waterfall, run-up, boom, tyre-cavity, gear-whine, e-motor-whine, transfer-path-analysis, tpa, otpa, blocked-force, noise-transfer-function, ntf, engine-mount, isolation, transmissibility, mode-map, modal-analysis, sound-quality, loudness, iso-532, accelerometer, binaural, simcenter, head-acoustics, nvh-cae]
level: practitioner
status: gated
description: "Diagnose a vehicle noise or vibration with source-path-receiver thinking: order tracking, mode maps, mount isolation rules and transfer-path analysis."
sources:
  - "van der Seijs, de Klerk & Rixen, 'General framework for transfer path analysis', MSSP 2016"
  - "ISO 532-1 (Zwicker loudness)"
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# NVH diagnosis: source → path → receiver

**Goal:** turn "there's a drone at about 100 km/h" into a named source, the dominant
path(s) and a fix ranked by cost — instead of adding foam until the complaint goes away.

## 1. Characterise the complaint at the receiver
- Reproduce it and record at the occupant: binaural head or microphones at driver/rear ear
  positions, plus tri-axial accelerometers on seat rail and steering wheel.
- Log rpm (engine and/or motor), vehicle speed, gear, throttle/torque, so data can be
  tracked against rotation, not just time.
- Note the subjective character: boom (low-frequency pressure), whine (tonal), rumble,
  harshness (impact), shake (tactile). Character often names the source.

## 2. Separate orders from resonances
Do a slow run-up (wide-open and light load) and plot a colour map of spectrum vs rpm
(waterfall/Campbell).
- **Lines that fan out from the origin** are orders: f = order × rpm / 60. They point
  to a rotating source.
- **Vertical bands at fixed frequency** are structural or acoustic resonances: the path
  or the receiver cavity amplifying whatever crosses them.
Common orders: 4-cylinder 4-stroke firing = 2nd engine order; 6-cylinder = 3rd (firing order = cylinders/2 for a four-stroke; computed); gear mesh
order = tooth count of the gear (on that shaft's speed); e-motor = multiples of pole-pair
count and slot number (e.g. a 48-slot, 8-pole machine shows strong 48th/96th orders),
plus inverter switching sidebands. Tyre/road: tyre cavity mode is typically ~180–250 Hz (f = c/(pi D_mean) with D_mean the mean cavity diameter: 189-245 Hz for 14-19 inch rims, computed),
fixed in frequency (depends on tyre size); wheel non-uniformity is 1st order of wheel
speed.

Example: boom peaking at 1800 rpm in a 4-cylinder car → 2nd order = 60 Hz. If the peak
stays at 60 Hz in every gear, it's a resonance (body panel or cabin acoustic mode) excited
by 2nd order; if it moves with rpm across gears it's source level.

## 3. Rank the paths
- **Quick screening:** disconnect or soften one path at a time (mount bypass, exhaust
  hanger removal, panel mass loading) and measure the change. Cheap and often decisive.
- **Isolation check per mount:** transmissibility drops below 1 only above f/fn = √2.
  Place mount system modes well below the lowest important excitation (rule of thumb:
  ratio ≥ ~2–3 (gated: unconfirmed, source is paywalled or blocked)). Example: idle 800 rpm, 2nd order = 26.7 Hz; rigid-body mount mode at
  12 Hz gives ratio 2.2 → undamped transmissibility 1/(r²−1) ≈ 0.25.
- **Dynamic stiffness ratio:** body-side attachment dynamic stiffness should be ≥ ~5–10× (gated: unconfirmed, source is paywalled or blocked)
  the mount stiffness at the frequency of interest, or the mount stops isolating.
  Measure attachment point inertance with an impact hammer.
- **Transfer-path analysis:** receiver response p = Σ NTF_i · F_i. Get NTFs (Pa/N) by
  hammer or reciprocally with a volume-velocity source; get operational forces by the
  mount-stiffness method (F = k_dyn · Δx across the mount), matrix inversion, or in-situ
  **blocked forces** (component-based TPA, transferable between vehicles). OTPA
  (operational, response-only) is fast but cross-talk between correlated paths can
  mislead — use it for screening, not sign-off.

## 4. Choose the fix by layer
1. **Source:** balance, order cancellation, gear micro-geometry, motor skew or pole
   shaping, inverter PWM strategy, torque-ripple control.
2. **Path:** mount rates and positions, tuned absorbers, attachment stiffness, panel
   damping, bushing tuning.
3. **Receiver:** acoustic package (barrier + absorber; ideal mass law gives ~6 dB per doubling
   of mass (gated: unconfirmed, source is paywalled or blocked)), seals, active noise cancellation.
Fixes closest to the source are usually cheapest per dB but slowest to change; acoustic
package fixes are quick but add mass and cost.

## 5. Judge with sound quality, not only dB(A)
Use loudness (sones, ISO 532-1 Zwicker method (gated: unconfirmed, source is paywalled or blocked)), articulation index, sharpness and tonality for whine.
A small tonal component can be more annoying than a broadband increase several dB higher.
EVs lose engine masking, so wind, road and auxiliary noise targets get tighter.

## Verify
- [ ] Complaint reproduced and recorded with rotational speed channels.
- [ ] Order vs resonance classified from a run-up map, checked across gears/loads.
- [ ] Mount isolation ratio and attachment dynamic stiffness checked for the key paths.
- [ ] Dominant paths ranked with TPA or controlled path-removal tests.
- [ ] Fix verified at the receiver by both level and sound-quality metrics, with no new
      issue in another speed range.
