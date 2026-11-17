---
id: defence-public-safety.forensic-science.trace-evidence-analysis.fibre-glass-paint-and-gsr-comparison
name: fibre-glass-paint-and-gsr-comparison
category: defence-public-safety
field: forensic-science
product: trace-evidence-analysis
tags: [trace-evidence-analysis, trace-evidence, fibres, fibers, fibre-comparison, tape-lifting, comparison-microscopy, polarised-light-microscopy, plm, microspectrophotometry, msp, ftir, raman, glass-analysis, refractive-index, grim, la-icp-ms, xrf, paint-analysis, paint-layers, pdq-database, py-gc-ms, gunshot-residue, gsr, sem-eds, lead-barium-antimony, transfer-and-persistence, contamination, evaluative-reporting, likelihood-ratio, locard]
level: advanced
status: draft
description: "Recover and compare trace evidence — fibres, glass, paint, gunshot residue: recovery order, the instrument sequence for each, contamination control and evaluating transfer and persistence."
sources: ["ASTM E1492/E2228 (fibres), E2927/E1967 (glass), E1610 (paint), E1588 (GSR by SEM-EDS)", "ENFSI Best Practice Manuals for fibres, glass and GSR", "Robertson, Roux & Wiggins, Forensic Examination of Fibres (textbook)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Fibre, glass, paint and GSR comparison

**Goal:** establish whether trace material recovered in a case could share an origin
with a known source, and how much that means given how easily such material transfers,
persists and turns up by chance.

## 1. Recovery comes first and decides everything
- **Order:** trace before fingermark powder or DNA swabbing where the item allows;
  agree a sequence with other disciplines.
- **Fibres:** tape-lift systematically (zonal lifts, each lift labelled by area) rather
  than scraping or picking; one-to-one taping for bodies/seats. Bag clothing separately.
- **Glass:** recover from clothing by shaking/brushing over clean paper in a dedicated
  room; collect a **control** from every broken source pane (frame-side marked).
- **Paint:** take controls with all layers down to substrate, from near the damage
  but undamaged area. Don't scrape just the top coat.
- **GSR:** sample hands/face/hair with carbon adhesive stubs **as early as possible** —
  most particles are lost from hands within hours with activity. Record time since
  incident and the subject's activity.
- **Contamination:** suspect and victim items examined in different rooms or at different
  times by different staff; examiners' clothing controlled. For GSR, police officers,
  vehicles and custody suites are known sources — sample blanks.

## 2. Analytical sequence (non-destructive → destructive)
**Fibres**
1. Low-power stereo search; select candidates against the control.
2. Comparison microscope (bright-field and fluorescence): colour, diameter,
   cross-section, delustrant.
3. Polarised light microscopy (generic class via birefringence).
4. **Microspectrophotometry** (UV-vis colour), then **FTIR or Raman** for polymer type.
5. Thin-layer chromatography of dyes only if the above can't discriminate (destructive).

**Glass**
- Refractive index (e.g. GRIM-type instrument) on fragments and multiple control points
  — panes vary. Elemental composition (µXRF, LA-ICP-MS) has far more discrimination.
- Use match criteria from your lab's validation (e.g. intervals based on control
  variability) — not a single eyeballed threshold.

**Paint**
- Layer sequence in cross-section under the microscope is the single most discriminating
  feature for automotive paint.
- FTIR per layer; Py-GC-MS for binders; SEM-EDS for pigments/extenders. PDQ (vehicle paint
  database) can suggest make/model/year range as a lead.

**GSR**
- SEM-EDS automated particle search; particles classified as **characteristic**
  (lead-barium-antimony, spheroidal morphology) or consistent-with. Heavy-metal-free
  primers are increasingly common — newer classification schemes cover them; check your
  scheme is current.

## 3. Evaluation, not just "match"
- "Indistinguishable from the control" is an analytical finding; its weight depends on
  how **common** the material is (white cotton is nearly worthless; an unusual dyed
  acrylic is not), on **transfer and persistence**, and on alternative explanations.
- Prefer **evaluative reporting** with explicit propositions (activity level: "he sat
  in the car" vs "he was never in the car") following ENFSI guidance; state the data
  your opinion relies on (population surveys, transfer studies).
- **GSR** cannot say who fired a weapon. Particles can come from being near a discharge,
  handling a weapon, or secondary transfer from a contaminated surface. Absence is weak
  evidence when sampling was late.

## Gotchas
- Glass on outer garments vs in pockets/turn-ups: location and number of fragments matter
  more than the match itself for activity questions.
- Paint smear from a vehicle collision may be a mixture of both vehicles' layers — sample
  both.
- Keep every lift and stub; re-examination by the defence is routine.

## Verify
- [ ] Recovery method, area and time recorded for every lift/stub.
- [ ] Controls taken from every potential source; blanks for GSR.
- [ ] Analysis followed non-destructive → destructive order.
- [ ] Match criteria come from validation, not judgment of the day.
- [ ] Report addresses commonness, transfer and persistence, with propositions stated.
