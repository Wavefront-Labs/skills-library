---
id: natural-sciences.physics.vacuum-cryogenic-technique.helium-leak-detection
name: helium-leak-detection
category: natural-sciences
field: physics
product: vacuum-cryogenic-technique
tags: [vacuum-cryogenic-technique, vacuum, high-vacuum, uhv, leak-detection, leak-hunting, helium-leak-detector, mass-spectrometer-leak-detector, mbar-l-s, leak-rate, spray-probe, sniffer, conflat, cf-flange, kf-flange, o-ring, viton, rate-of-rise, virtual-leak, outgassing, superleak, cold-leak, cryostat, dilution-refrigerator, turbopump, residual-gas-analyser, rga, pfeiffer, leybold, inficon]
level: practitioner
status: draft
description: "Find leaks in high-vacuum and cryostat systems with a helium mass-spectrometer leak detector: setup, spraying order, response time, cold leaks and virtual leaks."
sources: ["Pfeiffer Vacuum, The Vacuum Technology Book", "Leybold, Fundamentals of Leak Detection", "J. F. O'Hanlon, A User's Guide to Vacuum Technology (3rd ed.)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Helium leak detection

**Goal:** locate a leak quickly and confirm the system meets its leak spec
(often < 1×10⁻⁹ mbar·L/s for UHV/cryogenic work) instead of pumping for days
hoping the pressure will come down.

## 1. Is it a leak at all?
Close the pump valve and watch pressure rise (rate-of-rise test):
- **Linear rise** that continues indefinitely → real leak (or permeation).
- **Rise that curves over and flattens** → outgassing (water, adsorbed gas); bake or
  keep pumping.
- An RGA helps: air leak shows N₂ (28) and O₂ (32) at ~4:1; water (18) dominating
  means outgassing. Argon (40) at ~1% of N₂ also fingerprints air.
- **Virtual leaks** (trapped volumes: blind tapped holes without vent slots, double
  welds) behave like a slowly decaying leak and do not respond to helium.

## 2. Connecting the detector
- Attach the leak detector (Pfeiffer, Leybold, Inficon and others) to the
  chamber — at the foreline of the turbopump in counter-flow mode, or directly
  to the chamber. Helium back-diffuses through a turbopump well.
- Calibrate/self-test against the internal reference leak before starting.
- Note the background signal. A high He background usually means helium
  saturated the room or O-rings from earlier spraying; ventilate, wait.

## 3. Spraying technique
- Use a spray gun at **low flow**. You're looking for location, not volume.
- **Start at the top** of the system and work down (helium is light and rises),
  and start from the joints farthest from the detector port.
- Spray one joint at a time, wait for the response time (seconds for a direct
  connection; can be tens of seconds through a large chamber or long narrow lines),
  let the signal recover before moving.
- Suspects in rough order: recently opened flanges, feedthroughs (electrical, rotary,
  bellows), welds, valve seats and bonnets, viewports, KF clamps, gauges.
- Bag a component (plastic bag + helium) to test it as a whole; then narrow down.
- Sniffer mode (system pressurised with He, sniff outside) is for parts that can't be
  evacuated; it is ~100× less sensitive.

## 4. Fixing
- CF flanges: re-tighten in a star pattern to the spec; if still leaking, replace the
  copper gasket (never reuse), inspect knife edges for nicks.
- O-rings: clean, check for hair/lint/cuts, light (or no) grease on Viton.
- Do **not** "fix" with vacuum sealant (e.g. Torr Seal, Vacseal) unless you accept it's
  semi-permanent and not UHV-clean; it's a last resort.

## 5. Cryogenic specifics
- **Cold leaks / superleaks** only open below ~4 K or below the superfluid transition
  (2.17 K); room-temperature testing passes. Test at low temperature with the
  detector on the IVC, or by thermal cycling a suspect joint in LN₂.
- Indium seals: clean surfaces, fresh indium, even torque; re-tighten after first cooldown if specified.
- Never spray He on a cold cryostat assuming no harm: He adsorbs on cold surfaces and
  can mask or delay the signal.

## Gotchas
- Spraying near the detector's own exhaust or a leaking pump gives false positives.
- Helium permeates Viton O-rings; a slowly rising, broad signal after spraying an O-ring
  can be permeation rather than a leak.
- *Uncertainty note:* leak-rate specs and counter-flow behaviour depend on your detector
  and pumps; confirm with the instrument manual.

## Verify
- [ ] Rate-of-rise curve is understood (leak vs outgassing).
- [ ] Detector calibrated against its reference leak; background noted.
- [ ] Every joint sprayed with the response time respected.
- [ ] After repair, the integrated leak rate meets the specification.
- [ ] For cryostats, leak-tightness confirmed at operating temperature.
