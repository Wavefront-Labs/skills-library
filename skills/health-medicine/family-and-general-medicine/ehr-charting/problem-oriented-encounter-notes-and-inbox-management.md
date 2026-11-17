---
id: health-medicine.family-and-general-medicine.ehr-charting.problem-oriented-encounter-notes-and-inbox-management
name: problem-oriented-encounter-notes-and-inbox-management
category: health-medicine
field: family-and-general-medicine
product: ehr-charting
tags: [family-and-general-medicine, ehr-charting, ehr, emr, electronic-health-record, epic, cerner, oracle-health, athenahealth, eclinicalworks, emis, systmone, soap-note, apso, problem-oriented-medical-record, pomr, problem-list, clinical-coding, snomed-ct, icd-10, encounter-note, clinical-documentation, smartphrases, dot-phrases, templates, copy-forward, note-bloat, in-basket, inbox-management, results-inbox, order-entry, cpoe, e-and-m-coding, documentation-burden, primary-care]
level: practitioner
status: draft
description: "Write problem-oriented primary-care notes (SOAP/APSO), keep a clean coded problem list, use templates without note bloat, and triage the EHR inbox in a fixed daily routine."
sources: ["Weed, Medical records that guide and teach, NEJM 1968 (problem-oriented record)", "AMA STEPS Forward modules on EHR inbox management and team documentation", "CMS 2021 office/outpatient E/M documentation guidelines (MDM- or time-based)", "PRSB/RCGP guidance on good clinical record keeping"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

*General professional reference on clinical documentation workflow, not patient-specific or legal/billing advice. Vendor menus differ; local policy, coding rules and your EHR's training materials take precedence.*

# Problem-oriented encounter notes and EHR inbox management

**Goal:** notes a colleague can act on in 30 seconds, a problem list that is true, and an
inbox that is cleared daily without spilling into evenings. This is vendor-neutral; names
like SmartPhrases (Epic), dot-phrases or concepts/templates (EMIS, SystmOne) are the same idea.

## 1. Note structure
Use **SOAP**, or **APSO** (Assessment/Plan first) so the reader sees decisions first —
many EHRs let you reorder note sections.

- **Subjective:** the patient's story in a few lines; ICE; pertinent negatives that rule
  out red flags ("no weight loss, no night sweats").
- **Objective:** vitals and the focused exam; results reviewed today with values.
- **Assessment/Plan, by problem:** one heading per problem, each linked to a problem-list
  entry. For each: working diagnosis and certainty ("likely", "?"), differential if open,
  plan (meds with dose, tests, referrals), **safety-net given**, and follow-up interval.

## 2. Keep the problem list honest
- Code active problems (SNOMED CT or ICD-10 per your system); resolve/inactivate the stale
  ones at each chronic review. Downstream recalls, decision support, quality metrics and
  registries run off these codes — a free-text diagnosis in a note is invisible to them.
- Separate **active**, **significant past** and **minor/resolved**. Allergies and
  intolerances recorded as coded entries with the reaction type.
- Record "suspected" or "?" carefully — some systems code a query as the diagnosis.

## 3. Templates, macros and copy-forward
- Build short personal macros for repetitive text (safety-net wording, procedure notes,
  normal exam components), with **required blanks** (e.g. `***` in Epic) that block
  signing until filled.
- **Copy-forward is the main source of note bloat and error**: copied exam findings that
  weren't done today are a medicolegal and safety problem. If you copy, edit or delete
  every line that wasn't re-confirmed.
- Pull results/meds via live links rather than pasting static tables into every note.

## 4. Orders
- Order from the problem (problem-linked ordering) so indications attach automatically.
- Reconcile medications at every visit that changes them; stop the old dose when you
  change it — duplicate active prescriptions are a classic EHR error.
- Read interaction alerts rather than reflex-overriding; document the reason when you override.

## 5. Inbox routine (the part that burns clinicians out)
- Fixed times: e.g. 15–20 min mid-morning and end of day; don't graze all day.
- Order: critical results and urgent messages → other results → patient messages →
  refills → letters/FYI.
- Touch each item once: action, delegate (pooled team inbox for refills/forms with
  protocols), or file — "seen" is not an action. Use results-to-patient templates
  ("normal, no action").
- Set out-of-office **delegation** before leave so results don't sit unread.
- Ask your EHR team to suppress pure-FYI notifications that need no action.

## 6. Coding the visit (US-style billing context)
Since 2021, office E/M level is chosen by **medical decision-making or total time** on the
date of service — history/exam bullet counting no longer sets the level. Document MDM
elements (problems addressed, data reviewed, risk of management) or total time explicitly.
Other countries use different schemes; skip if not applicable.

## Gotchas
- Note signed late or never: unsigned notes may be invisible to colleagues and are a
  compliance issue — close encounters the same day.
- Dictation/voice-recognition errors ("hypo-" vs "hyper-", "no" dropped): proofread A/P.
- Patients can read their notes (open notes/patient portal access): write plainly and
  avoid judgemental language.
- Problem-list entries added by other teams may be wrong — verify before propagating.
- Uncertainty: feature names, signing behaviour and inbox folders vary by vendor and build.

## Verify
- [ ] Every problem in A/P maps to a coded problem-list entry.
- [ ] No copied-forward findings that weren't reassessed today.
- [ ] Medication list reconciled; no duplicate active doses.
- [ ] Safety-net and follow-up stated per problem.
- [ ] Note signed same day; inbox cleared to zero actionable items by end of day.

Related: `health-medicine.family-and-general-medicine.care-coordination-and-referral.referral-letters-and-test-results-safety-netting`.
