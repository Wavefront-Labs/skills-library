---
id: health-medicine.oncology.radiation-therapy-systems.linac-image-guided-treatment-delivery
name: linac-image-guided-treatment-delivery
category: health-medicine
field: oncology
product: radiation-therapy-systems
tags: [linac, linear-accelerator, igrt, image-guided-radiotherapy, cbct, cone-beam-ct, kv-imaging, portal-imaging, epid, imrt, vmat, treatment-planning-system, tps, record-and-verify, oncology-information-system, immobilisation, immobilization, thermoplastic-mask, surface-guided-radiotherapy, sgrt, 4d-ct, deep-inspiration-breath-hold, dibh, mlc, multileaf-collimator, patient-specific-qa, brachytherapy-afterloader, hdr, aapm-tg-142]
level: practitioner
status: draft
description: "Run the linac treatment chain safely: CT simulation and immobilisation, TPS plan checks, record-and-verify, IGRT/CBCT matching with tolerances, motion management and QA."
sources: ["AAPM Task Group 142 report: Quality assurance of medical accelerators", "AAPM TG-179 and TG-218 reports (CT-based IGRT QA; IMRT patient-specific QA tolerances)", "RCR/SCoR/IPEM On target 2: updated guidance for image-guided radiotherapy", "Khan's The Physics of Radiation Therapy (textbook)", "IAEA safety reports on prevention of accidental exposure in radiotherapy"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

> General clinical/professional reference, not a substitute for independent clinical judgement, current guidelines, or verified dosing references.

# Linac image-guided treatment delivery

**Goal:** get the planned dose to the right place in the right patient every fraction,
using the linac, planning system and imaging chain with independent checks at each hand-off.

## 1. Simulation and immobilisation
- **CT simulation** in the treatment position on a flat couch top with indexed
  immobilisation: thermoplastic mask (head and neck, brain), breast board, vacuum bag,
  knee/foot rests. Reproducibility matters more than comfort tweaks made later.
- Record set-up reference marks (tattoos or surface-guidance reference) and bladder or
  rectal preparation instructions where relevant (pelvis).
- **Motion management:** 4D-CT for lung/liver to build an ITV; **deep inspiration breath
  hold (DIBH)** for left breast to reduce heart dose; abdominal compression or gating as
  appropriate.

## 2. Planning system (TPS) and plan checks
- Planner optimises (3D-conformal, IMRT or VMAT) to the prescription and OAR
  constraints; clinician approves.
- **Independent plan check** by a physicist or dosimetrist: correct patient, CT
  dataset, isocentre, prescription (dose, fractions, energy), calculation algorithm and
  grid, density overrides, couch inclusion, and an independent monitor-unit/dose
  verification.
- **Patient-specific QA** for IMRT/VMAT: phantom or EPID-based measurement with gamma
  analysis against tolerances per local policy (AAPM TG-218 recommends commonly used
  criteria such as 3%/2 mm with action levels; confirm local standard).

## 3. Record-and-verify (R&V / oncology information system)
- Plan exported to the R&V system, which locks machine parameters (MU, MLC, gantry,
  energy, couch) and blocks delivery outside tolerance.
- **Never override an R&V interlock** without understanding and documenting why; many
  historical radiotherapy incidents involved data transfer or manual overrides.
- First-day check: plan, set-up instructions, and imaging protocol verified by two
  radiographers/therapists.

## 4. Image guidance at the machine
- **Positive patient identification** (at least two identifiers, photo) at every
  fraction.
- Set up to marks/surface guidance, then image: **kV planar**, **CBCT** (soft tissue),
  MV portal (EPID), or surface-guided radiotherapy (SGRT) for continuous monitoring.
- **Match to the reference** on the agreed surrogate: bone for many sites, fiducial
  markers for prostate, soft tissue for bladder/cervix. Apply couch shifts (6 degrees of
  freedom where available).
- Use the **departmental IGRT protocol** for imaging frequency, action levels and
  tolerances (for example: correct shifts above a set threshold; escalate shifts beyond
  an action level to the planner or clinician). Protocols follow national guidance
  such as "On target 2"; values are site-specific.
- Watch for anatomical change (weight loss in head and neck, tumour shrinkage, bladder
  filling) which may require **adaptive replanning**.

## 5. Machine QA
- Daily, monthly and annual linac QA per **AAPM TG-142** or national equivalents: output
  constancy, laser and imaging isocentre coincidence, MLC position, safety interlocks,
  CBCT geometric accuracy.
- Do not treat on a machine with a failed daily QA until a physicist clears it.

## 6. Brachytherapy afterloaders (outline)
HDR afterloaders drive a sealed source (commonly Ir-192) through applicators per the
TPS plan. Key controls: source-strength verification on exchange, applicator
reconstruction checks, emergency source-retraction procedures rehearsed and emergency
kit at hand, radiation surveys after each treatment.

## Gotchas
- Wrong-isocentre and wrong-plan errors usually arise at hand-offs, not in the plan.
- Matching to bone when the target moves relative to bone (prostate, cervix) gives a
  false sense of accuracy.
- Imaging dose from frequent CBCT is not zero; follow the justified protocol.
- A mask that no longer fits after weight loss invalidates the PTV margin.

## Verify
- [ ] Immobilisation and motion management documented and reproducible.
- [ ] Independent plan check and patient-specific QA passed before first fraction.
- [ ] R&V parameters match the approved plan; no undocumented overrides.
- [ ] Patient identified and imaged per IGRT protocol; shifts within action levels.
- [ ] Daily machine QA passed; anatomical changes flagged for adaptive review.
