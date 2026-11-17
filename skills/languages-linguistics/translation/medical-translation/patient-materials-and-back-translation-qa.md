---
id: languages-linguistics.translation.medical-translation.patient-materials-and-back-translation-qa
name: patient-materials-and-back-translation-qa
category: languages-linguistics
field: translation
product: medical-translation
tags: [medical-translation, translation, pharmaceutical-translation, life-sciences-translation, clinical-trials, informed-consent, icf, patient-information-leaflet, pil, smpc, qrd-templates, ema, patient-reported-outcomes, pro, coa, linguistic-validation, back-translation, reconciliation, cognitive-debriefing, readability, health-literacy, medical-terminology, meddra, iso-17100]
level: advanced
status: draft
description: "Translate clinical and patient-facing material safely: right register for patients vs clinicians, regulatory templates, and back-translation with reconciliation for consent forms and questionnaires."
sources: ["ISPOR Task Force principles for translation and cultural adaptation of PRO measures (Wild et al. 2005)", "EMA QRD templates for product information (ema.europa.eu)", "ISO 17100:2015"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Patient materials and back-translation QA

**Goal:** medical translations where no error can reach a patient: correct terminology for
professional texts, plain understandable language for patients, regulator-mandated wording
where it exists, and documented QA (often back-translation) where the client or sponsor
requires it.

## 1. Identify the text type — it sets the rules
- **Professional** (SmPC, clinical study protocol, case report forms, journal articles):
  precise terminology, standard abbreviations, formal register.
- **Patient-facing** (informed consent forms, patient information leaflets, instructions for
  use, appointment letters): plain language at a low reading level, short sentences,
  everyday words ("high blood pressure", not "hypertension") — matching the source's
  intended reading level.
- **Regulated templates**: EU product information follows EMA QRD templates with fixed
  headings and standard phrases in each official language — use the current template text
  verbatim. *Other regulators have their own requirements; check the target market.*
- **Clinical outcome assessments / PRO questionnaires**: need *linguistic validation*, not just
  translation (below).

## 2. Terminology
- Use recognised sources: regulatory glossaries, national pharmacopoeia names, MedDRA terms
  for adverse events when the client codes with it, INN drug names (not brand names unless in source).
- Dosage: never alter numbers, units or decimal placement; render "q.d.", "b.i.d." per target
  convention and avoid ambiguous abbreviations (e.g. "U" for units, trailing zeros like "1.0 mg"
  are classic dosing-error risks).
- Anatomical left/right, negation ("not recommended" vs "recommended"), and frequency words
  (common, very common — often defined frequency bands in product information) must be exact.

## 3. Linguistic validation workflow (typical for PROs and some ICFs)
1. **Two independent forward translations** by native target-language translators.
2. **Reconciliation** into one version by a third person, with documented reasons.
3. **Back-translation** into the source language by a translator who hasn't seen the source.
4. **Review/harmonisation**: compare back-translation with source; investigate every
   meaning discrepancy (not style); amend the forward version.
5. **Cognitive debriefing**: interview a handful of target-population patients (often 5–8) to
   check they understand items as intended.
6. Proofread and **document everything** in a report — sponsors and regulators may audit it.
Back-translation detects meaning shifts; it does not prove the target reads naturally.

## 4. Cultural adaptation
Questionnaire items about activities ("walking a block", "climbing a flight of stairs",
specific foods, units of measure) may need culturally equivalent examples. Changes must be
justified and approved by the instrument developer where licensed.

## Gotchas
- Back-translators who "fix" toward the source they guess at hide real problems.
- Over-technical patient material: a correct but unreadable consent form fails ethically.
- Copy-paste from old approved versions after the source changed — diff the source first.
- Many instruments are copyrighted; translation requires the developer's permission.
- Data privacy: patient records carry health data; use secure channels and follow the client's
  rules on MT and cloud tools.

## Verify
- [ ] Text type identified and the matching template/glossary used.
- [ ] Numbers, units, doses, left/right and negations checked line by line against source.
- [ ] Patient-facing text checked for plain language by a non-specialist reader.
- [ ] Where required: two forward translations, reconciliation, back-translation, review and
      debriefing are documented with decisions.
- [ ] Final version matches the latest source revision.

Related: `languages-linguistics.translation.translation-revision.bilingual-revision-and-mqm-error-typology`,
`languages-linguistics.translation.technical-translation.terminology-consistency-and-controlled-language`.
