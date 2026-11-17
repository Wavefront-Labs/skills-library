---
id: manufacturing-production.production-quality-control.cmm-programming.writing-and-running-a-cmm-part-program
name: writing-and-running-a-cmm-part-program
category: manufacturing-production
field: production-quality-control
product: cmm-programming
tags: [cmm-programming, cmm, coordinate-measuring-machine, pc-dmis, calypso, zeiss-calypso, modus, camio, metrolog, polyworks, probe-qualification, reference-sphere, stylus, tip-calibration, probe-head, renishaw, ph10, cad-based-programming, alignment, 3-2-1-alignment, datum-reference-frame, gd-t, position, profile, flatness, feature-construction, best-fit, clearance-plane, collision, sampling-strategy, scanning, touch-trigger, inspection-report, dmis, first-article, production-quality-control]
level: practitioner
status: draft
description: "Program and run a production CMM job: qualify the probe, build the datum alignment from the drawing, measure features with sensible sampling, evaluate GD&T and produce a report people trust."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Writing and running a CMM part program

**Goal:** a repeatable CMM program that measures what the drawing actually controls,
in the drawing's datum frame, and runs unattended on production parts without
crashing the probe. Examples use Hexagon PC-DMIS and Zeiss CALYPSO terms; Renishaw MODUS,
Nikon CAMIO and Metrologic Metrolog XG follow the same steps. Uncertainty budgeting is in
engineering-technology.technical-authentication-testing.dimensional-metrology.cmm-inspection-and-uncertainty-budgets.

## 1. Before programming
- **Read the drawing first** — list datums (A, B, C), each feature control frame, and
  which characteristics are critical/special. The program serves the drawing, not the CAD model.
- Check the CAD model revision matches the drawing revision.
- Plan **fixturing**: part stable, repeatable location, all features reachable, no
  clamping distortion on thin parts. Note fixture and orientation in the program header.
- Thermal: part and machine soaked to the room (20 °C reference); a part straight from a
  machining centre can be several degrees warm — let it soak or use temperature compensation if fitted.

## 2. Probe qualification
- Build the probe/stylus configuration (stylus length, tip diameter, extensions) in software.
- **Qualify** every tip angle used against the **reference sphere**: the software
  reports tip diameter and form/standard deviation — compare with your limit (e.g. a
  few µm; site-specific). A bad result = loose stylus, dirty sphere or dirty tip.
- Requalify after any crash, stylus change, or per schedule.

## 3. Alignment (the step that makes or breaks results)
- **Manual/rough alignment**: few points by joystick to locate the part roughly.
- **DCC alignment** following the drawing's **datum reference frame**: primary datum
  (plane from ≥3 points, better spread) levels; secondary (line/plane/cylinder)
  rotates; tertiary sets origin. Use the actual datum features, not convenient faces.
- Iterate the alignment in DCC mode for best accuracy.
- Datum features of size (holes, bosses) referenced at MMB modify how much the part can
  shift — use the software's datum-shift/best-fit evaluation if the drawing calls for it.

## 4. Measuring features
- Pick points from CAD or teach them; **sampling**: enough points for the form you
  care about (e.g. a hole: 4 points gives a size, 8+ or a scan gives roundness meaningfully).
- **Scanning** for profile, flatness and form; touch-trigger for size/location on simple features.
- Measure at the right **depth** in holes (mid-depth or both ends if perpendicularity/position over length matters).
- Set **clearance planes** and approach/retract distances; avoid tight moves near walls.
- Construct features (e.g. a line through two hole centres, a plane from points) only as the drawing implies.

## 5. Evaluating and reporting
- Use the software's **GD&T evaluation** (Position, Profile, Flatness, Perpendicularity)
  with the drawing's modifiers (MMC/LMC, projected zone, datum references) — not just
  XYZ deviations. Profile of a surface relative to datums is not the same as best-fit form.
- Report: characteristic number (ballooned drawing), nominal, tolerance, actual,
  deviation, pass/fail. Export to the QMS/SPC system (e.g. CSV, Q-DAS) if used.

## 6. Proving the program
- Run in **slow speed/step mode** first, hand on the stop.
- Run the same part **several times** (repeatability) and with re-fixturing (reproducibility);
  results should be within a small fraction of tolerance — formal MSA per
  manufacturing-production.production-quality-control.measurement-system-analysis.running-a-gage-rr-and-acting-on-it.
- Compare a few results with an independent method (height gauge, bore gauge).
- Lock the released program; changes via revision control.

## Gotchas
- Aligning on a convenient machined face instead of the drawing datum.
- Ignoring a probe qualification standard deviation that crept up.
- Too few points on a feature then reporting form.
- Evaluating position without the datum modifiers specified.
- Unattended runs after a fixture change without a dry run → crash.

## Verify
- [ ] Probe tips qualified today within limit.
- [ ] Alignment matches drawing datum frame and order.
- [ ] Each characteristic on the ballooned drawing appears once in the report with its tolerance.
- [ ] Repeat runs agree within a small fraction of tolerance.
- [ ] Program revision released and matches drawing/CAD revision.
