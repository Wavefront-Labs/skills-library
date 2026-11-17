---
id: health-medicine.cardiology.echocardiography-systems.tte-standard-views-doppler-measurement-and-tee-acquisition
name: tte-standard-views-doppler-measurement-and-tee-acquisition
category: health-medicine
field: cardiology
product: echocardiography-systems
tags: [cardiology, echocardiography-systems, echocardiography, tte, transthoracic-echo, tee, toe, transoesophageal-echo, cardiac-sonographer, standard-views, parasternal-long-axis, apical-four-chamber, subcostal, suprasternal, biplane-simpson, lvot-measurement, continuous-wave-doppler, pulsed-wave-doppler, tissue-doppler, pedoff, speckle-tracking, strain-package, contrast-echo, ultrasound-enhancing-agent, philips-epiq, ge-vivid, siemens-acuson]
level: practitioner
status: draft
description: "Echo system acquisition: TTE standard views and optimisation, PW/CW/tissue Doppler measurement technique, LVOT and Simpson's pitfalls, strain packages, contrast, and TOE acquisition workflow."
sources: [ASE guidelines for performing a comprehensive transthoracic echocardiographic examination 2018, BSE minimum dataset for TTE (2020), ASE/SCA comprehensive TEE guidelines 2013, EACVI/ASE strain standardisation task force 2015, vendor operator manuals (generic features)]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# TTE standard views, Doppler measurement and TOE acquisition

> General clinical/professional reference, not a substitute for lab protocols, vendor manuals or supervised training. Menu names differ between Philips, GE, Siemens, Canon and others.

**Goal:** a complete, reproducible dataset where each measurement is taken from the
right view with the right technique — measurement error, not machine error, drives most
wrong echo conclusions.

## 1. Set-up
- Patient details (height/weight for indexing, BP at time of study), ECG leads for timing,
  left lateral decubitus for parasternal/apical windows.
- Phased-array transducer, cardiac preset; harmonics on; adjust depth, sector width
  (narrow for frame rate), gain/TGC, focus; frame rate ≥ ~50 fps for strain.
- Store ≥ 3 cardiac cycles (more in AF; ≥ 5 beats averaged for Doppler in AF).

## 2. Standard TTE views (minimum dataset)
- **Parasternal long axis (PLAX):** LV dimensions/wall thickness (2D-guided, perpendicular
  to LV long axis at mitral leaflet tips), **LVOT diameter** (zoomed, mid-systole, inner
  edge to inner edge, within ~0.5–1 cm of the annulus), aortic root.
- **Parasternal short axis:** aortic valve level (cusps, RVOT, PA), mitral, papillary
  muscle, apex.
- **Apical 4-, 2-, 3-chamber:** avoid foreshortening (apex should be thin and stationary;
  move down an interspace and lateral). **Biplane Simpson's** traced on non-foreshortened
  A4C/A2C; use contrast if ≥ 2 contiguous segments aren't seen.
- **Subcostal:** IVC size/collapse, pericardial effusion, atrial septum.
- **Suprasternal:** aortic arch, descending aorta flow.
- Right-sided views (RV-focused A4C) for RV size and TAPSE.

## 3. Doppler technique
- **Alignment is everything:** Doppler underestimates velocity when the beam isn't
  parallel to flow; angle correction is **not** used in cardiac Doppler.
- **PW Doppler:** LVOT VTI with the sample volume just proximal to the valve (avoid flow
  acceleration), mitral inflow at leaflet tips (E/A), pulmonary veins.
- **CW Doppler:** aortic stenosis from **multiple windows** (apical, right parasternal with
  the **Pedoff**/non-imaging probe, suprasternal, subcostal) — the highest velocity counts.
  TR velocity from several views for PASP.
- **Tissue Doppler:** septal and lateral e′ with sample volume at the annulus, low gain
  and low velocity scale.
- Sweep speed 100 mm/s for measurements; scale set so the envelope fills ~2/3 of display.

## 4. Strain and 3D packages
- Speckle-tracking GLS from the three apical views at good frame rate; check tracking in
  every segment and adjust the ROI; don't compare values across vendors.
- 3D full-volume acquisitions need breath-hold and regular rhythm (stitching artefacts).

## 5. Contrast (ultrasound-enhancing agents)
Indicated for poor endocardial definition, LV thrombus or apical HCM suspicion. Low-MI
contrast preset, slow infusion or small boluses; screen contraindications per label and
observe per local policy.

## 6. TOE acquisition workflow
- Indication, fasting, consent, oesophageal pathology screening (dysphagia, varices,
  prior surgery), sedation plan (see
  `health-medicine.anesthesiology.sedation-and-monitored-care.procedural-sedation-depth-titration-and-rescue`).
- Probe check (no damage, electrical safety), bite guard.
- Standard levels: mid-oesophageal (4-chamber, commissural, 2-chamber, long-axis, aortic
  valve short/long axis, bicaval, LAA with multiplane sweep), transgastric, upper and
  descending aorta views.
- LAA: image at ≥ 2 angles (0°, 45°, 90°, 135°) to exclude thrombus; check emptying velocity.
- Post-procedure: nil by mouth until throat anaesthesia wears off; probe cleaning and
  high-level disinfection logged.

## Gotchas
- LVOT diameter errors are squared in continuity equation AVA.
- Foreshortened apical views inflate EF and hide apical thrombus.
- Single-window CW in AS underestimates severity.

## Verify
- [ ] Height/weight, BP and ECG captured.
- [ ] Minimum dataset views stored; apical views not foreshortened.
- [ ] LVOT measured correctly; AS interrogated from multiple windows.
- [ ] Doppler gain/scale/sweep optimised; AF averaged over ≥ 5 beats.
- [ ] TOE probe checked before and disinfection logged after.
