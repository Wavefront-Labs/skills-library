---
id: engineering-technology.biomedical-engineering.medical-imaging-systems.ct-dose-and-image-quality-tradeoffs
name: ct-dose-and-image-quality-tradeoffs
category: engineering-technology
field: biomedical-engineering
product: medical-imaging-systems
tags: [computed-tomography, ct, ctdivol, ctdiw, dlp, effective-dose, ssde, mas, kvp, pitch, image-noise, cnr, mtf, nps, iterative-reconstruction, deep-learning-reconstruction, atcm, tube-current-modulation, diagnostic-reference-levels, drl, acr-ct-phantom, catphan, iec-60601-2-44, dose-check, protocol-optimisation]
level: advanced
status: gated
description: "Balance CT dose and image quality: CTDIvol/DLP/SSDE, how mAs, kVp, pitch and slice thickness drive noise and CNR, ATCM, iterative recon, MTF/NPS phantom tests and DRL checks."
sources: ["AAPM Report 96: The Measurement, Reporting, and Management of Radiation Dose in CT (https://www.aapm.org/pubs/reports/RPT_96.pdf)", "AAPM Report 204 (https://www.aapm.org/pubs/reports/detail.asp?docid=143) and Report 220 (https://www.aapm.org/pubs/reports/detail.asp?docid=146): size-specific dose estimates", "AAPM Dose Check guidelines (https://www.aapm.org/pubs/ctprotocols/documents/notificationlevelsstatement.pdf)", "IEC 60601-2-44 Particular requirements for X-ray equipment for computed tomography (confirm edition)", "NEMA XR 25 Computed Tomography Dose Check", "ACR CT Accreditation Program (https://www.imagewisely.org/Imaging-Modalities/Computed-Tomography/Accreditation-of-Your-CT-Program)", "Bushberg et al., The Essential Physics of Medical Imaging (4th ed.)", "ICRP Publication 135: Diagnostic reference levels in medical imaging"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CT dose and image-quality trade-offs — the least dose that answers the clinical question

**Goal:** set or evaluate a CT protocol so image quality is sufficient for the diagnostic task at the lowest reasonable dose, with metrics that can be measured and audited.

Engineering guidance; clinical protocols are approved by the radiologist and medical physicist under local regulations.

## 1. Dose metrics

- **CTDIw** = ⅓·CTDI100,centre + ⅔·CTDI100,periphery, measured with a 100 mm pencil chamber in a PMMA phantom: 16 cm (head) or 32 cm (body).
- **CTDIvol** = CTDIw / pitch (helical). It is a *scanner output* index, not patient dose. Always note which phantom is referenced (paediatric bodies are sometimes reported against 16 cm, doubling the number).
- **DLP** = CTDIvol × scan length (mGy·cm).
- **Effective dose** E ≈ k × DLP, adult k (mSv/mGy·cm) from the AAPM Report 96 conversion table: head 0.0021, chest 0.014, abdomen and pelvis 0.015 (read from the report PDF; 32 cm phantom factors for body, 16 cm for head). Population-level estimate only; do not quote it for an individual.
- **SSDE** = CTDIvol(32) × f(water-equivalent diameter) per AAPM 204/220; small patients get conversion factors > 1.

## 2. Parameter physics

| Parameter | Effect on dose | Effect on image |
|---|---|---|
| mAs | ∝ mAs | noise σ ∝ 1/√mAs (halve noise = 4× dose) |
| kVp | roughly ∝ kVp^2.5-3 at fixed mAs | lower kVp raises iodine contrast, raises noise; CNR for iodine often improves at 80-100 kV in small/average patients |
| Pitch | CTDIvol ∝ 1/pitch at fixed mA | with "effective mAs" (mAs/pitch) held, noise roughly constant; high pitch reduces motion, may add helical artefacts |
| Slice thickness | no dose change | σ ∝ 1/√thickness; thin slices for detail, thick for low-contrast |
| Recon kernel | none | sharp kernel raises MTF and noise |

**Low-contrast detectability** depends on CNR and object size; **high-contrast resolution** depends on MTF (focal spot, detector size, kernel), not dose.

## 3. ATCM (automatic tube current modulation)

Modulates mA in z and angle from the localiser attenuation. Vendors use either a reference quality mAs (e.g. CARE Dose4D-type) or a target noise index (GE-type); know which, because their behaviour with patient size differs. Patient **centring** matters: off-centre positioning mis-scales the localiser and bowtie, changing dose and noise by tens of percent. Scan the localiser in the direction your vendor recommends (e.g. PA to reduce breast dose on some systems).

## 4. Reconstruction

Iterative (vendor products such as ASiR-V, SAFIRE/ADMIRE, iDose, AIDR 3D (gated: unconfirmed, source is paywalled or blocked)) and deep-learning (TrueFidelity, AiCE-class (gated: unconfirmed, source is paywalled or blocked)) reconstruction reduce noise at a given dose, but shift the **NPS** to lower frequencies (blotchy texture) and can make MTF contrast- and dose-dependent. Equal pixel σ does not mean equal detectability: evaluate with task-based metrics (detectability index d′, model observers) or reader studies before cutting dose by the noise ratio.

## 5. Measure image quality

- **ACR CT phantom / Catphan:** water CT number and uniformity tolerances per the current ACR CT QC manual (the commonly quoted ±7 HU and ±5 HU limits are (gated: unconfirmed, source is paywalled or blocked)), noise, CT-number linearity, low-contrast objects, high-contrast bar patterns, slice thickness.
- **MTF:** wire/bead (PSF) or edge (ESF) method; report MTF50 and MTF10.
- **NPS:** from uniform-region ROIs (2D FFT of mean-subtracted ROIs), report peak frequency and integral.
- **CNR** = |HU_object − HU_bg| / σ_bg at matched slice thickness and kernel.

## 6. Benchmark against DRLs and safety features

Compare median CTDIvol and DLP per protocol and patient-size band with national DRLs (ACR-AAPM, EU/UK national DRLs). For ACR accreditation, ImageWisely (ACR/RSNA/AAPM) lists ACR pass/fail CTDIvol values of 80 mGy adult head, 30 mGy adult abdomen and 25 mGy paediatric abdomen, which it labels the 2008 values; ACR has since revised its dosimetry document, so check the current ACR values. Above-DRL medians trigger review; below-DRL is not automatically "good" if image quality fails.

IEC 60601-2-44 requires dose display (CTDIvol, DLP) and, with NEMA XR 25, **Dose Check** notification and alert values (the AAPM Dose Check guidelines cite an FDA-suggested CTDIvol alert value of 1000 mGy, roughly half the dose associated with skin injury onset; notification values are set per protocol and are user-configurable).

## Gotchas

- CTDIvol does not scale with patient size; a small child at the same CTDIvol gets a higher dose. Use SSDE.
- Changing kVp with ATCM on can silently change mA; re-check noise and dose together.
- Comparing noise across vendors requires same slice thickness, kernel and recon type.
- Perfusion and repeated-location scans: watch CTDIvol for deterministic skin effects.

## Verify

- [ ] CTDIvol, DLP and SSDE recorded with phantom size stated.
- [ ] Noise, CNR and MTF measured on phantom at protocol settings and match acceptance criteria.
- [ ] Iterative/DL recon dose reduction backed by task-based or reader evaluation.
- [ ] ATCM type and reference setting documented; centring checked.
- [ ] Protocol medians compared with current national DRLs per size band.
- [ ] Dose Check notification/alert values configured.
