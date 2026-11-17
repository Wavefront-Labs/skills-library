---
id: manufacturing-production.production-quality-control.production-ndt.in-line-penetrant-mag-particle-ultrasonic-and-leak-test-stations
name: in-line-penetrant-mag-particle-ultrasonic-and-leak-test-stations
category: manufacturing-production
field: production-quality-control
product: production-ndt
tags: [production-ndt, ndt, non-destructive-testing, nde, dye-penetrant, liquid-penetrant, fluorescent-penetrant, fpi, astm-e1417, magnetic-particle, mpi, mt, wet-fluorescent, astm-e1444, ketos-ring, field-indicator, demagnetisation, ultrasonic-testing, ut, immersion-ut, phased-array, reference-blocks, leak-testing, pressure-decay, mass-flow-leak, helium-leak, bubble-test, leak-master, system-verification, iso-9712, nas-410, asnt-snt-tc-1a, operator-certification, production-quality-control]
level: practitioner
status: draft
description: "Run NDT as a production check: daily system verification for penetrant, mag-particle, UT and leak-test stations, reading indications, rejecting correctly, and the certification rules."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# In-line penetrant, mag-particle, ultrasonic and leak test stations

**Goal:** the NDT station on your line finds the defects it's meant to find, every
shift — which means proving the system works before trusting a "pass". Field/maintenance
NDT (aircraft, structures) is covered in
repair-maintenance.aircraft-maintenance.non-destructive-testing.dye-penetrant-and-eddy-current-crack-inspection;
this is the high-volume production version.

## 0. Who may do what
NDT results are only valid from **certified** personnel: ISO 9712 (general industry),
NAS 410/EN 4179 (aerospace), or employer-based ASNT SNT-TC-1A. Level 1 performs to a written
technique; Level 2 sets up, interprets and accepts/rejects; Level 3 writes procedures.
Production operators may load/unload, but interpretation needs the right level — confirm your site's written practice.

## 1. Liquid penetrant (surface-breaking defects, any non-porous material)
Sequence: pre-clean (dry, oil-free) → penetrant (dwell, e.g. 10–30 min per spec) →
remove excess (water-wash, or emulsifier then wash — time is critical; over-washing pulls
penetrant from cracks) → dry → developer → development time → inspect.
- **Fluorescent (FPI)**: UV-A intensity at the part surface ≥ 1000 µW/cm² and white light
  in the booth ≤ 2 fc (≈ 20 lx) — typical ASTM E1417 values; inspector dark-adapted (~1 min or per spec).
- **Daily checks**: known-defect panel (e.g. TAM/PSM-5 panel) shows all its indications
  at expected brightness; UV meter reading; developer coverage; penetrant contamination/water content per schedule.

## 2. Magnetic particle (surface/near-surface, ferromagnetic only)
- Wet fluorescent particles on a horizontal bench; **two directions of magnetisation**
  (head shot for longitudinal defects, coil shot for transverse) — a crack parallel to the field is invisible.
- **Daily**: bath concentration (centrifuge tube settling — e.g. 0.1–0.4 mL per 100 mL for fluorescent), contamination check,
  Ketos ring or known-defect part to show system sensitivity, field indicator (pie gauge/
  QQI shims) on the part, ammeter verification per schedule.
- **Demagnetise** after inspection where required; check residual field with a gaussmeter
  (e.g. ≤ 3 gauss is a common limit, spec-specific).

## 3. Ultrasonic (internal defects, thickness)
- Immersion or contact; phased-array systems on automated cells.
- **Calibrate/verify** at start and per interval (and after any probe/cable change)
  against **reference blocks** with known reflectors (flat-bottom or side-drilled holes);
  set gain so the reference reflector hits the reference amplitude, then apply the
  reject threshold.
- Couplant consistency matters; dry spots look like missing signals, which a gate can read as "no defect".
- If a verification fails, all parts since the last good verification are **suspect** and re-inspected.

## 4. Leak testing
- **Pressure decay**: pressurise, stabilise, measure pressure drop over test time;
  sensitive to temperature (warm parts from washing give false results) and fixture seals.
- **Mass flow**: measures make-up flow; faster for larger volumes.
- **Helium/tracer gas**: very small leak rates (e.g. refrigeration, EV battery, medical).
- **Bubble/immersion**: simple, operator-dependent.
- **Daily**: run a **leak master** (calibrated orifice giving a known leak) to prove the
  tester rejects, and a known-good part to prove it accepts. Watch fixture seal wear.

## 5. Rejects and records
- Rejected parts tagged and moved to the locked reject area; never re-test until pass
  without a defined retest rule (repeat-until-pass hides real leaks).
- Record verification results, parameters and part counts per shift; parts tested since
  the last successful verification are only as good as that verification.

## Gotchas
- Inspecting FPI in a booth with a door open (ambient light kills sensitivity).
- Over-washing penetrant to "clean up" background.
- Only one magnetisation direction because the second shot takes time.
- UT gain raised to hide noise, then never reset.
- Leak test on parts still warm from washing.

## Verify
- [ ] Your certification level covers what you're doing.
- [ ] Start-of-shift system checks passed and recorded (known-defect panel, Ketos ring/shims, reference block, leak master).
- [ ] Process parameters (dwell, wash, current, gain, test pressure/time) match the written technique.
- [ ] Rejects tagged and segregated; no repeat-until-pass.
- [ ] A failed verification triggered re-inspection back to the last good check.
