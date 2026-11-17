---
id: health-medicine.allied-health-technologies.radiography-and-ct-systems.positioning-exposure-technique-and-ct-dose-practice
name: positioning-exposure-technique-and-ct-dose-practice
category: health-medicine
field: allied-health-technologies
product: radiography-and-ct-systems
tags: [allied-health-technologies, radiography-and-ct-systems, radiographer, radiologic-technologist, x-ray, ct, computed-tomography, patient-positioning, exposure-factors, kvp, mas, exposure-index, deviation-index, aec, collimation, alara, ctdivol, dlp, tube-current-modulation, iso-centering, contrast-injection, pregnancy-check, diagnostic-reference-levels]
level: practitioner
status: draft
description: "Radiography and CT technologist practice: ID and pregnancy checks, positioning, kVp/mAs and exposure index, collimation, CT iso-centering, dose modulation, CTDIvol/DLP and reference levels."
sources: [ACR-AAPM practice parameters for radiography and CT, ICRP Publication 135 diagnostic reference levels, Image Gently / Image Wisely campaigns, vendor CT dose-management documentation (generic)]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Positioning, exposure technique and CT dose practice

> General clinical/professional reference, not a substitute for local protocols, vendor manuals or the supervising radiologist/medical physicist. Exact technique values depend on equipment and patient.

**Goal:** a diagnostic image on the first attempt at the lowest reasonable dose —
repeats are the biggest avoidable dose source.

## 1. Before every exposure
1. **Two-identifier patient ID** and match to the request (right patient, right exam,
   right side — mark laterality before exposure).
2. **Pregnancy status** for people of reproductive age in or near the primary beam per
   local policy; document.
3. Remove artefacts (jewellery, clothing with metal, gown snaps).
4. Explain breathing instructions and practise them.
5. CT with contrast: renal function per policy, allergy/prior reaction history,
   cannula size and position, metformin rules per local guideline.

## 2. Radiography technique
- **kVp** drives penetration and contrast; **mAs** drives receptor exposure (and dose).
  Digital systems tolerate overexposure silently — "dose creep".
- Use the vendor **exposure index (EI)** and **deviation index (DI)**: DI near 0 is on
  target; roughly ±1 corresponds to ~25% over/under. Track repeat causes.
- **AEC:** select the right chambers for the anatomy; a misplaced chamber over a
  prosthesis or outside the anatomy gives the wrong exposure.
- **Collimate to the anatomy** and keep collimation visible on the image; electronic
  cropping after exposure hides overexposed tissue.
- Use a grid for thick parts (roughly > 10–12 cm); remove it for small extremities.
- Positioning: centre the central ray on the stated landmark, align the part with
  the receptor, and use immobilisation aids instead of holding patients (if a person must
  hold, never staff routinely; shield and document).

## 3. CT practice
- **Iso-centre the patient** in the gantry: off-centre positioning interacts with
  bowtie filters and tube current modulation, raising dose and noise.
- Scout/topogram covers the full planned range; **tube current modulation** uses it,
  so scan direction and arms position (arms up for chest/abdomen) matter.
- Scan range exactly as protocol — every extra centimetre is dose.
- Use age/size-based protocols (paediatric protocols mandatory for children).
- Check the console's **CTDIvol and DLP** before scanning and against local
  **diagnostic reference levels**; dose-notification values prompt a deliberate pause.
- Contrast timing: bolus tracking ROI placement and threshold per protocol; check
  injector line for air, extravasation watch during injection.

## 4. After the exposure
- Review image quality before the patient leaves: anatomy included, rotation, motion,
  markers, EI/DI.
- Record repeats and reason (positioning, motion, technique) for QA.
- Send to PACS with correct accession; flag urgent findings per local escalation.

## Gotchas
- Wrong-side markers added digitally after the event cause medico-legal problems — place
  lead markers at exposure.
- Pediatric scans on adult protocols remain a recurring dose incident.
- Gonad shielding is no longer routinely recommended in many jurisdictions (it often
  obscures anatomy and interferes with AEC) — follow your current national guidance.

## Verify
- [ ] ID, laterality, pregnancy and contrast checks documented.
- [ ] EI/DI within target; collimation visible; marker correct.
- [ ] CT: iso-centred, range limited, CTDIvol/DLP reviewed vs DRLs.
- [ ] Repeat logged with cause; images sent and urgent findings escalated.
