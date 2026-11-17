---
id: health-medicine.ophthalmology.ophthalmic-imaging-systems.oct-acquisition-and-artefact-recognition
name: oct-acquisition-and-artefact-recognition
category: health-medicine
field: ophthalmology
product: ophthalmic-imaging-systems
tags: [oct, optical-coherence-tomography, sd-oct, swept-source-oct, oct-angiography, octa, spectralis, cirrus, topcon, macular-cube, rnfl, ganglion-cell-analysis, segmentation-error, segmentation-artifact, artefact, artifact, signal-strength, decentration, mirror-artefact, motion-artefact, eye-tracking, follow-up-scan, progression-analysis, normative-database, central-subfield-thickness, fundus-photography]
level: practitioner
status: draft
description: "Acquire good OCT macular, RNFL and OCTA scans, recognise segmentation and acquisition artefacts, and run valid longitudinal comparisons on registered follow-up scans."
sources: ["Duker, Waheed and Goldman: Handbook of Retinal OCT (textbook)", "AAO Basic and Clinical Science Course: Retina and Vitreous, and Glaucoma (imaging chapters)", "Manufacturer user manuals for OCT platforms (general reference)", "Chhablani and colleagues: review literature on OCT artefacts (general reference)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

> General clinical/professional reference, not a substitute for independent clinical judgement, current guidelines, or verified dosing references.

# OCT acquisition and artefact recognition

**Goal:** produce scans good enough to trust, spot the artefacts that fake disease or hide
it, and compare visits in a way that measures real change rather than scan noise.

## 1. Prepare and acquire
- Dilate where helpful (small pupils, cataract, peripheral or widefield scans); clean
  lens; ask the patient to blink just before capture to refresh the tear film.
- Enter correct **refraction/focus** and axial length or eye length where the device uses
  it for scaling.
- Select the protocol for the question:
  | Question | Typical protocol |
  |---|---|
  | Macular oedema, AMD, holes, ERM | Macular volume/cube plus high-density line scans through fovea |
  | Glaucoma | Peripapillary RNFL circle scan plus macular ganglion cell analysis |
  | Neovascularisation, ischaemia | OCT angiography (OCTA) cube |
  | Disc swelling | Optic nerve head volume, RNFL |
- Use **eye tracking** and averaging (where available); keep the target centred and
  wait for good signal before capturing.
- Check **signal strength/quality index** against the manufacturer's minimum; repeat
  poor scans before the patient leaves.

## 2. Review every scan for artefacts
| Artefact | Look for | Consequence |
|---|---|---|
| **Segmentation error** | Boundary lines jumping off the true layer, especially with fluid, ERM, high myopia, PED | False thickness and false progression |
| **Decentration** | Foveal pit not in centre grid; RNFL circle off-centre on disc | Wrong central subfield thickness, sectoral RNFL errors |
| **Low signal / media opacity** | Dim, grainy B-scans, cataract, asteroid hyalosis | Global thinning, unreliable maps |
| **Motion** | Discontinuities, doubled vessels on en face/OCTA | Spurious defects |
| **Mirror/inverted image** | Image folded at top of frame in long eyes | Misread structure |
| **Projection (OCTA)** | Superficial vessels appearing in deeper slabs | False choroidal neovascularisation |
| **Blink/floaters** | Black bands or shadows | Local pseudo-defects |
Never rely on the colour-coded summary page alone; scroll the B-scans and correct
segmentation manually where the software allows.

## 3. Interpret against the right reference
- Normative databases are age-matched but often exclude high myopia, very small or large
  discs, and some ethnic groups. "Red" on a myopic tilted disc can be normal
  (**red disease**); "green" can hide early damage (**green disease**).
- Read thickness maps together with the B-scan morphology (fluid type: intraretinal,
  subretinal, sub-RPE).

## 4. Longitudinal comparison
- Use the device's **follow-up mode** so scans register to the baseline location.
- Compare scans on the **same device and software version**; thickness values are not
  interchangeable across manufacturers.
- Change smaller than the device's test-retest variability is noise; check
  manufacturer or literature repeatability values before calling progression.
- Trend analysis (e.g. RNFL slope over several visits) is more robust than single-pair
  differences. Note the RNFL **floor effect** in advanced glaucoma: switch emphasis to
  macular ganglion cell and visual fields.

## Gotchas
- Wrong patient demographics (date of birth) apply the wrong normative band.
- Re-baselining after cataract surgery is needed: signal improves and apparent
  thickness changes.
- OCTA flow absence can be signal loss, not true non-perfusion.

## Verify
- [ ] Protocol matches clinical question; signal quality above minimum.
- [ ] B-scans reviewed; segmentation and centration checked and corrected.
- [ ] Interpretation accounts for normative database limits.
- [ ] Follow-up scans registered, same device, change exceeds repeatability.
