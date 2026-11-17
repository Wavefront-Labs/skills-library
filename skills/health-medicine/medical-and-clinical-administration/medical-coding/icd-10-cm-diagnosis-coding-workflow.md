---
id: health-medicine.medical-and-clinical-administration.medical-coding.icd-10-cm-diagnosis-coding-workflow
name: icd-10-cm-diagnosis-coding-workflow
category: health-medicine
field: medical-and-clinical-administration
product: medical-coding
tags: [medical-coding, medical-and-clinical-administration, icd-10-cm, icd-10, icd-11, diagnosis-coding, alphabetic-index, tabular-list, excludes1, excludes2, code-first, use-additional-code, principal-diagnosis, sequencing, physician-query, coding-guidelines, outpatient-coding, inpatient-coding, cpc, ccs]
level: practitioner
status: gated
description: "ICD-10-CM coding method: abstract the record, Index→Tabular every time, apply conventions (Excludes1/2, code first, 7th characters), sequence by setting, and query when documentation is unclear."
sources: ["https://www.cms.gov/files/document/fy-2027-icd-10-cm-coding-guidelines.pdf", "https://www.cdc.gov/nchs/icd/icd-10-cm/files.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ICD-10-CM diagnosis coding workflow

> General clinical/professional reference, not a substitute for independent clinical judgement, current guidelines, or verified dosing references.

**Goal:** assign the complete, correctly sequenced set of diagnosis codes the
documentation supports — no more, no less — in a way an auditor can retrace.

Scope note: written for US ICD-10-CM (diagnoses). Procedure coding uses CPT/HCPCS
(professional/outpatient) or ICD-10-PCS (inpatient facility). Other countries use
ICD-10 modifications (ICD-10-AM, ICD-10-CA) or ICD-11 with different rules — the method
transfers, the conventions do not. Code sets update every **1 October** (FY; the FY 2027 guidelines apply to encounters from 1 October 2026 to
30 September 2027); always
code against the edition valid for the date of service.

## 1. Know the setting first
- **Inpatient facility:** principal diagnosis = condition *established after study* to
  be chiefly responsible for the admission. Uncertain diagnoses ("probable",
  "suspected", "rule out") documented at discharge **are coded as if confirmed** (gated: unconfirmed, source is paywalled or blocked).
- **Outpatient/professional:** first-listed = main reason for the encounter. **Do not
  code uncertain diagnoses** — code the signs/symptoms instead (gated: unconfirmed, source is paywalled or blocked).

## 2. Abstract the record
Read the whole encounter: H&P, progress notes, discharge summary, operative report,
results *interpreted by the provider*. You code from provider documentation — a lab
value alone (e.g. low sodium) cannot be coded as hyponatraemia unless the provider
documents the diagnosis.

## 3. Look up: Alphabetic Index → Tabular List, always
1. Find the main term (the condition, not the anatomy: "fracture", not "femur").
2. Follow subterms and cross-references ("see", "see also").
3. **Verify in the Tabular List** — never code from the Index alone. The Tabular holds
   the instructional notes and full character requirements.

## 4. Apply the conventions (gated: unconfirmed, source is paywalled or blocked)
- **Excludes1:** the two conditions are never coded together (mutually exclusive) —
  except where the guidelines allow when unrelated.
- **Excludes2:** "not included here" — both may be coded if both present.
- **Code first / use additional code:** etiology/manifestation pairs (e.g. diabetic
  conditions, infections with organisms). Manifestation codes (often italic, "in
  diseases classified elsewhere") cannot be principal.
- **Combination codes** beat multiple codes when one code captures both elements
  (e.g. diabetes with specified complication).
- **"With"/"in"** in the Index presumes a causal link (e.g. diabetes and CKD) unless the
  provider documents another cause.
- **7th characters** (A initial, D subsequent, S sequela for injuries) and the
  placeholder **X** when a code has fewer than six characters but needs a 7th.
- Code to the **highest specificity** documented (laterality, type, acuity, stage).

## 5. Sequence and finish
Principal/first-listed, then secondary diagnoses that affect care (inpatient:
conditions requiring clinical evaluation, treatment, diagnostic tests, extended LOS
or increased nursing care). Add status, history and external-cause codes per guidelines
and payer requirements.

## 6. Query when the record is unclear
Query the provider for conflicting, incomplete, ambiguous or illegible
documentation, or when clinical indicators support an undocumented diagnosis. Queries
must be **non-leading**: present clinical indicators, offer clinically reasonable
options including "other" and "unable to determine", and never mention reimbursement.

## Worked micro-example
Inpatient: "Admitted with sepsis due to E. coli UTI; acute kidney injury." → Sepsis
due to E. coli (A41.51) principal, UTI (N39.0) secondary, AKI (N17.9) (gated: unconfirmed, source is paywalled or blocked). Verify each in
the Tabular and check current guideline/Coding Clinic sequencing (and severe sepsis
codes if organ dysfunction is linked) — codes given as illustration only.

## Gotchas
- Coding from a problem list copy-forward without evidence of current relevance.
- Unspecified codes when the documentation actually gives specificity (laterality!).
- Using last year's code book after 1 October.
- Assigning a code because an encoder suggested it without reading the Tabular notes.

## Verify
- [ ] Setting identified and uncertain-diagnosis rule applied accordingly.
- [ ] Every code traced Index → Tabular with notes checked.
- [ ] Excludes1, code-first and 7th-character rules satisfied.
- [ ] Sequencing follows the official guidelines for the setting.
- [ ] Ambiguities resolved by compliant, non-leading queries, not assumptions.

## Checked

- Date checked: 2026-10-25. Jurisdiction: United States (ICD-10-CM, FY 2027).
- Sources read: Search-result summaries of the CMS FY 2027 guidelines page; the guidelines PDF itself came back as binary.
- Confirmed: That the FY 2027 guidelines cover encounters from 1 Oct 2026 to 30 Sep 2027 and contain uncertain-diagnosis sections in both the inpatient (II.H) and outpatient (IV.H) parts.
- Corrected or removed: Removed the unsupported "large share of errors" claim.
- Gated: The wording of II.H and IV.H, the Excludes1/Excludes2, with/in, 7th-character conventions and the three example codes, because the guideline text and code tables could not be read.

Method: documentation only; no commands were run.
