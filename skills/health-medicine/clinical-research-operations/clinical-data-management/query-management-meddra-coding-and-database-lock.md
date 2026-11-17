---
id: health-medicine.clinical-research-operations.clinical-data-management.query-management-meddra-coding-and-database-lock
name: query-management-meddra-coding-and-database-lock
category: health-medicine
field: clinical-research-operations
product: clinical-data-management
tags: [clinical-data-management, clinical-research-operations, cdm, data-management-plan, crf-design, ecrf, edit-checks, query-management, data-cleaning, medical-coding, meddra, whodrug, smq, sae-reconciliation, database-lock, soft-lock, hard-lock, cdash, sdtm, cdisc, gcdmp, ich-e6-r3, protocol-deviation-listing]
level: practitioner
status: draft
description: "Keep trial data clean to lock: edit-check and query workflow, MedDRA/WHODrug coding conventions, SAE reconciliation, and a database-lock readiness checklist."
sources:
  - "Society for Clinical Data Management, Good Clinical Data Management Practices (GCDMP)"
  - "MedDRA Term Selection: Points to Consider (ICH, current release)"
  - "MedDRA Introductory Guide (MSSO, current release)"
  - "Uppsala Monitoring Centre, WHODrug Global user documentation"
  - "CDISC CDASH Implementation Guide and SDTM Implementation Guide"
  - "ICH E6(R3) Guideline for Good Clinical Practice (Step 4, January 2025)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Query management, MedDRA coding and database lock

*General clinical/professional reference, not a substitute for independent clinical judgement, current guidelines, or verified dosing references.*

**Goal:** a trial database whose critical data are complete, plausible, consistently
coded and reconciled, locked on a documented date with every outstanding item resolved
or explicitly accepted.

## 1. Set up for cleanliness
- **Data management plan (DMP):** CRF completion guidelines, edit-check spec, coding
  dictionaries and versions, reconciliation scope, lock criteria, roles.
- CRF design input: collect only protocol-required data; CDASH-aligned fields map cleanly
  to SDTM; avoid free text where a codelist works; one concept per field; units explicit.
- **Edit checks:** range (e.g. SBP 60-250 mmHg — soft, query), consistency (AE end date ≥
  start date), cross-form (con-med indication has a matching AE or medical-history entry),
  protocol logic (visit date inside window). Test in UAT before go-live.

## 2. Query workflow
1. Auto-queries fire on entry; manual queries from data review, SDV or medical review.
2. Write queries that are **neutral and specific**: "AE start 12-Mar precedes first dose
   14-Mar; please confirm or correct" — never lead ("please change to…").
3. Site answers or corrects in EDC; DM reviews and closes or re-queries.
4. Track ageing: e.g. target response ≤10 working days; escalate via CRA beyond 30 days
   (targets are study-specific).
5. Avoid query storms: tune noisy checks rather than issuing hundreds of low-value queries.

## 3. Medical coding
| Data | Dictionary | Code to |
|---|---|---|
| AEs, medical history, indications | **MedDRA** (SOC → HLGT → HLT → PT → LLT) | LLT, which maps to one PT and a primary SOC |
| Con-meds | **WHODrug Global** | Drug name / preferred base, ATC class |

MedDRA *Points to Consider* rules worth memorising:
- Code what was reported; do not add or subtract information (no diagnosis from symptoms
  unless the reporter gave one).
- If a diagnosis and its signs are reported together, code the diagnosis (signs optional per conventions).
- Query ambiguous verbatims ("bad turn", "reaction") rather than guessing.
- Keep one MedDRA version per analysis; MedDRA updates twice yearly (March, September) —
  plan up-versioning and re-review changed terms before lock.
- Use **SMQs** for safety analysis across many PTs.

## 4. Reconciliation
- **SAE reconciliation:** safety database vs EDC — case ID, PT, onset, seriousness,
  causality, outcome must match; discrepancies to both safety and site.
- External data: central lab, ECG, IRT randomisation and dosing, ePRO — reconcile keys
  (participant, visit, date) and transfer counts.
- Protocol-deviation listing reviewed and classified before lock.

## 5. Database lock
Checklist (all signed off):
- [ ] All expected data entered; missing pages/visits explained.
- [ ] All queries closed (or documented as unresolvable).
- [ ] SDV/SDR complete per monitoring plan; investigator e-signatures on casebooks.
- [ ] Coding complete and medically reviewed; dictionary versions recorded.
- [ ] SAE and external-data reconciliation complete.
- [ ] Blinded data review meeting held; analysis populations agreed.
- [ ] **Soft lock** → final checks → **hard lock**; access removed; lock date documented.
Unlocking requires written justification, approval and audit trail.

## Gotchas
- Cleaning to "make the data look right" is falsification; queries must go to the site.
- Changing coding conventions mid-study without recoding creates split terms in tables.
- Lab units and reference ranges differ by site — normalise before range checks.
- Late external data transfers are the commonest cause of lock slippage.

## Verify
- [ ] DMP, edit-check spec and coding conventions approved before first data entry.
- [ ] Open-query ageing report reviewed weekly.
- [ ] Coding reviewed by a medically qualified person.
- [ ] SAE reconciliation shows zero unexplained discrepancies.
- [ ] Lock checklist signed and filed in TMF.
