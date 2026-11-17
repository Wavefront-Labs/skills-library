---
id: repair-maintenance.aircraft-maintenance.non-destructive-testing.dye-penetrant-and-eddy-current-crack-inspection
name: dye-penetrant-and-eddy-current-crack-inspection
category: repair-maintenance
field: aircraft-maintenance
product: non-destructive-testing
tags: [aircraft-maintenance, non-destructive-testing, ndt, ndi, dye-penetrant, liquid-penetrant, fluorescent-penetrant, astm-e1417, developer, dwell-time, eddy-current, ect, bolt-hole-probe, pencil-probe, impedance-plane, reference-standard, calibration-block, crack-detection, nas410, en4179, magnetic-particle, ultrasonic-thickness]
level: practitioner
status: draft
description: "Find surface cracks on aircraft parts with liquid penetrant (clean, dwell, remove, develop) and eddy current probes calibrated on a reference standard; method choice and reporting."
sources: ["ASTM E1417 Standard Practice for Liquid Penetrant Testing", "FAA AC 43.13-1B ch. 5 Nondestructive Inspection", "NAS 410 / EN 4179 (NDT personnel qualification)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dye penetrant and eddy current crack inspection

**Goal:** detect surface-breaking (and, with eddy current, near-surface) cracks reliably
and report them with location and size. NDT on aircraft must be done to the specific
NDT manual procedure for the part (aircraft NDT manual / SRM / SB) by personnel
qualified to NAS 410 or EN 4179 at the right level. This skill explains the methods
so you can perform and understand them under that system.

## Choosing the method
| Method | Finds | Materials | Notes |
|---|---|---|---|
| Liquid penetrant (PT) | Surface-open cracks | Any non-porous | Paint must be removed; cheap, slow |
| Eddy current (ET) | Surface & near-surface cracks, conductivity, corrosion thinning | Conductive (aluminium, titanium, steel) | Through thin paint; needs reference standard |
| Magnetic particle (MT) | Surface & near-surface | Ferromagnetic steel only | Demagnetise after |
| Ultrasonic (UT) | Internal flaws, thickness | Most | Needs couplant, skill |
| Radiography (RT) | Internal, assemblies | All | Radiation safety |

## 1. Liquid penetrant (Type II visible or Type I fluorescent)
1. **Pre-clean:** strip paint (chemical stripper; abrasive blasting and sanding smear
   metal over cracks — if done, etch per spec before PT). Degrease with solvent; dry fully.
2. **Apply penetrant** by spray or brush to cover the area plus a margin.
3. **Dwell:** typically 10–30 min at 10–52 °C (ASTM E1417 ranges; your procedure decides).
   Keep it wet — don't let it dry on.
4. **Remove excess:** solvent-removable method — wipe with a dry lint-free cloth, then a
   cloth *dampened* with remover, wiping one direction. **Never spray remover directly
   on the part** — it washes penetrant out of the cracks.
5. **Develop:** thin, even coat of non-aqueous developer from ~30 cm; too thick masks
   small indications. Develop time ~10 min (minimum per procedure).
6. **Interpret:** visible dye → bright red lines on white in good white light; fluorescent
   → UV-A lamp (≥ 1,000 µW/cm² at the surface is a common requirement) in a darkened area
   (≤ 20 lux) after eye adaptation.
   - Linear indication (length > 3× width) = crack candidate. Rounded = porosity.
   - Re-clean and re-test anything doubtful; wipe with a solvent swab — a real crack
     bleeds back.
7. Post-clean all residue (developer is corrosive in crevices) and restore finish.

## 2. Eddy current (pencil and bolt-hole probes)
**Kit:** impedance-plane instrument (e.g. Olympus Nortec-class), probe of the right frequency
(high frequency 100 kHz–2 MHz for surface cracks in aluminium; lower for subsurface), a
**reference standard** of the same alloy with EDM notches (e.g. 0.008, 0.020, 0.040 in deep).
1. Null the probe on unflawed reference material; set lift-off to a horizontal signal
   (rotate the phase so lift-off moves left/right).
2. Scan the reference notch; adjust gain so the target notch gives a specified screen
   height (e.g. 50–80 % of full screen) and the crack signal is vertical-ish, distinct
   from lift-off.
3. Set an alarm gate if the instrument has one.
4. Scan the part at the same speed and probe angle; overlap scans by ~50 % of probe
   footprint. Use a guide/template along fastener rows and edges.
5. **Bolt-hole:** remove the fastener, clean the hole, use a rotating scanner at the
   specified rpm; sweep the full depth of the bore in steps.
6. Recheck calibration on the reference at the end (and every ~30 min); if drifted,
   re-inspect everything since the last good check.

## Reporting
Record part/serial, area, method/procedure number, equipment and reference standard ID,
indications with location (station/stringer, clock position in a hole), length, and
disposition. Sketch or photograph.

## Gotchas
- Penetrant contaminates the part for later ET/UT and can't follow anodise sealing;
  sequence methods correctly.
- Edge effect and fastener signals in ET look like cracks; compare to an identical
  location on the other side.
- Uncertain: dwell times, UV intensity and notch sizes here are typical; the procedure
  for your part controls.

## Verify
- [ ] Method chosen suits the defect type and material; procedure number recorded.
- [ ] PT: paint removed, dwell met, excess removed by damp-wipe only, thin developer.
- [ ] ET: calibrated on matching reference standard; recal check at end passed.
- [ ] Every indication located, sized, dispositioned and reported; part post-cleaned.
