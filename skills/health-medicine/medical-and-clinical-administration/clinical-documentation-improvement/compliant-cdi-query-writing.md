---
id: health-medicine.medical-and-clinical-administration.clinical-documentation-improvement.compliant-cdi-query-writing
name: compliant-cdi-query-writing
category: health-medicine
field: medical-and-clinical-administration
product: clinical-documentation-improvement
tags: [clinical-documentation-improvement, medical-and-clinical-administration, cdi, cdi-query, physician-query, compliant-query, acdis, ahima, clinical-indicators, severity-of-illness, risk-of-mortality, ms-drg, apr-drg, cc-mcc, hcc, clinical-validation, multiple-choice-query, documentation-review]
level: practitioner
status: gated
description: "Write non-leading CDI queries: when a query is warranted, building clinical indicators, open-ended vs multiple-choice formats, forbidden wording, clinical-validation queries and tracking responses."
sources: ["https://acdis.org/system/files/resources/DES-1622_ACDIS-AHIMA_Guidelines-Compliant-Query-Practice_positionpaper.pdf", "https://ahima.org/media/51ufzhgl/20221212_acdis_practice-brief.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Compliant CDI query writing

> General clinical/professional reference, not a substitute for independent clinical judgement, current guidelines, or verified dosing references.

**Goal:** get the provider to document what they actually think — accurately, specifically
and completely — without leading them toward any particular (or higher-paying) answer.

## 1. Is a query warranted?
Query when the record is:
- **Conflicting** (e.g. "systolic HF" in one note, "HFpEF" in another);
- **Incomplete or ambiguous** (e.g. "respiratory failure" without acuity; "anaemia"
  with transfusion but no type);
- **Clinically supported but undocumented** (indicators present, diagnosis not stated);
- **Clinically unsupported** (diagnosis documented without indicators → clinical
  validation query);
- **Illegible**, or a present-on-admission (POA) status is unclear.
Don't query to "improve" a record that is already clear, or for conditions with no
bearing on care.

## 2. Build the clinical indicators
Pull dated, sourced facts from the *current encounter*: vitals, labs, imaging, provider
assessments, treatments, nursing observations. Example for possible acute
hypoxic respiratory failure: "SpO₂ 86% on room air (ED triage, 14:05); RR 32; started on
4 L nasal cannula then high-flow 40 L/min FiO₂ 0.6; accessory muscle use noted by RN."
Prior-encounter data may support a query but cannot be its sole basis; sufficient support must exist in the current encounter.

## 3. Choose the format
- **Open-ended:** "Based on the clinical indicators above, please clarify the
  diagnosis being treated." Least leading; slower responses.
- **Multiple choice:** list clinically reasonable options supported by the indicators,
  **plus** "other (please specify)" and "unable to determine" (and "clinically
  undetermined") (gated: unconfirmed, source is paywalled or blocked). Example options: acute hypoxic respiratory failure / hypoxaemia
  without respiratory failure / other / unable to determine.
- **Yes/No:** allowed **only** for POA status, substantiating a diagnosis already
  present in the record (e.g. confirming a consultant's diagnosis), establishing cause
  and effect, or resolving conflicting documentation between providers. Never for a
  new, undocumented diagnosis, and not to confirm or negate a complication of care. Include an
  "unable to determine" option.
- **Clinical validation query:** "Documentation states sepsis; clinical indicators in
  the record include… Please confirm or rule out the diagnosis" with options including
  "ruled out".

## 4. Wording rules (what makes a query non-compliant)
- No mention of reimbursement, DRG, CC/MCC, SOI/ROM, quality scores or audits.
- No introducing a diagnosis not supported by indicators.
- No leading phrasing ("Please document sepsis to accurately reflect…").
- No implying any impact of the answer, or that the provider is being judged.
- Neutral tone, specific to this patient; templates must be adapted, not pasted.

## 5. Process
- Deliver by the organisation's approved method (EHR query, verbal with documentation).
  Verbal queries must be documented like written ones.
- The answer must be documented **in the medical record** (progress note/discharge
  summary or a query form retained as part of the permanent record per policy).
- Escalation policy for unanswered queries (e.g. 48 h → physician advisor).
- Track: query rate, response rate, agreement rate, time to response, by topic and
  provider; audit a sample of queries for compliance quarterly.

## Gotchas
- Asking "Is the patient malnourished?" when no dietitian assessment or indicators
  exist is leading.
- Listing only the highest-weighted option plus "other" is leading by omission.
- Don't code from a query answer that contradicts the rest of the record without
  further clarification.
- Clinical criteria (e.g. Sepsis-2 vs Sepsis-3) may differ between provider practice
  and payer audit policies — document the definition used.

## Verify
- [ ] Query reason fits one of the warranted categories.
- [ ] Indicators are dated, sourced and from this encounter.
- [ ] Format appropriate; multiple choice includes other/unable to determine.
- [ ] No financial, leading or judgemental wording.
- [ ] Response captured in the permanent record and tracked.

## Checked

- Date checked: 2026-10-25. Jurisdiction: United States (ACDIS/AHIMA practice brief).
- Sources read: Search-result summaries of the AHIMA-hosted 2022 brief and the ACDIS 2026 update; the 2026 position-paper PDF returned binary text.
- Confirmed: The 2022 brief limits yes/no queries to POA status, substantiating an already documented diagnosis, cause and effect, and resolving conflicting documentation, requires an "unable to determine" option, and bars yes/no for undocumented diagnoses.
- Corrected or removed: The 2026 update supersedes the 2022 brief: yes/no is inappropriate for complications of care, and prior-encounter information cannot be the sole basis; both added and sources repointed. Removed the I.A.19 ICD-10-CM citation (not confirmed).
- Gated: The multiple-choice option list incl. "clinically undetermined", the reimbursement-wording ban and the other process items, because the 2026 text could not be read.

Method: documentation only; no commands were run.
