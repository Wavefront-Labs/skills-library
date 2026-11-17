---
id: manufacturing-production.pharmaceutical-manufacturing.equipment-qualification.executing-iq-oq-pq-protocols
name: executing-iq-oq-pq-protocols
category: manufacturing-production
field: pharmaceutical-manufacturing
product: equipment-qualification
tags: [equipment-qualification, qualification, validation, iq, oq, pq, dq, fat, sat, commissioning, c-and-q, protocol-execution, test-scripts, acceptance-criteria, protocol-deviation, process-validation, ppq, process-performance-qualification, stage-2, cpv, continued-process-verification, requalification, periodic-review, change-control, annex-15, astm-e2500, asme-bpe, gamp-5, csv, pharmaceutical-manufacturing, gmp]
level: practitioner
status: docs-checked
description: "Execute qualification protocols on the production side: pre-checks, IQ/OQ/PQ test steps, evidence capture, protocol deviations, PPQ batch support and requalification."
sources:
  - "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/process-validation-general-principles-and-practices"
  - "https://health.ec.europa.eu/medicinal-products/eudralex/eudralex-volume-4_en"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Executing IQ/OQ/PQ protocols

**Goal:** generate qualification evidence that is complete, contemporaneous and
defensible, so the equipment or process can be released for GMP use — and spot problems
the protocol didn't anticipate. Framework: EU GMP Annex 15 (Qualification and validation) and the FDA process validation
guidance (January 2011); confirm any other standard you apply.

## 1. What each stage proves
| Stage | Question | Typical tests |
|---|---|---|
| **IQ** Installation | Is it what we bought, installed as designed? | Model/serial, materials of construction certificates, P&ID walk-down, utilities connected, calibration of instruments, drawings and manuals filed |
| **OQ** Operational | Does it work across its operating range? | Alarms and interlocks, setpoint control at low/high, sequence logic, speed/temperature ranges, power failure recovery, user access levels |
| **PQ** Performance | Does it perform consistently with real (or simulated) load? | Repeated runs with product/placebo, mapping, outputs meeting specification |
| **PPQ** (process validation Stage 2, process qualification) | Does the commercial process reproducibly make good product? | Commercial-scale batches with enhanced sampling; the number is justified by the manufacturer |
FAT/SAT and commissioning results can be leveraged into IQ/OQ when the quality unit agrees and documents it.

## 2. Before executing
- Protocol **approved** (all signatures) and the version you hold is the effective one.
- Pre-requisites met: previous stage closed or approved with open items assessed;
  instruments used for testing **in calibration** (record IDs and due dates); SOPs and
  training for operators in place; change control open.
- Read each test step and its **acceptance criterion** before the run. If a criterion is
  ambiguous ("works correctly"), raise it before execution, not after.

## 3. Executing
- Do the step exactly as written; record **actual** results (values, not "pass"),
  initials and date for each step, and attach evidence (screenshots, printouts, photos
  where allowed). Number attachments and reference them in the step.
- Pass/fail is decided against the stated criterion only.
- One step, one result: don't batch-fill a page of results at the end of the day.
- Test witnesses (QA/engineering) sign where the protocol calls for it, while watching.

## 4. When something fails or doesn't fit
- **Stop**, record what actually happened, and raise a **protocol deviation/discrepancy**
  (separate from a GMP batch deviation in many QMSs).
- Classify impact; agree re-test scope with the protocol owner and QA. Don't re-run a
  failed step until the cause is understood and the retest is authorised.
- Fixing the equipment (new setting, new part) may need a change control and could
  invalidate earlier steps — check.
- Typos or genuinely wrong protocol instructions are also deviations; don't silently
  execute "what they meant".

## 5. PPQ batches from the production floor
- Enhanced sampling: extra samples at specified times/locations — set reminders, missed
  samples can't be recreated.
- Run the process at the target conditions in the batch record; don't "help" the batch
  with unusual attention — PPQ must reflect routine operation.
- Record everything that would be a normal deviation; a PPQ batch with deviations may
  still pass but they need assessment.

## 6. After go-live
- **Requalification / periodic review** per schedule or after significant changes
  (relocation, major repair, software update).
- **Change control** before any change to qualified equipment, including "like for like" parts — let the system decide if it's like-for-like.
- Continued process verification (Stage 3 of the FDA guidance) trends what PPQ proved.

## Gotchas
- Executing from an unapproved draft protocol (everything done is void).
- Using an instrument that went out of calibration mid-execution.
- Screenshots without timestamp or system identity.
- OQ alarms tested by "observing" rather than actually forcing the condition.

## Verify
- [ ] Approved protocol version; prerequisites signed.
- [ ] Every step has actual result, pass/fail, initials, date, and referenced evidence.
- [ ] Test instruments' calibration IDs and due dates recorded and valid on execution dates.
- [ ] Every failure or unexpected result has a protocol deviation with agreed resolution.
- [ ] Summary report traces each acceptance criterion to evidence.

## Checked

Date: 2026-10-25. Jurisdictions: United States (FDA guidance Process Validation: General Principles and Practices, January 2011, final) and European Union (EudraLex Volume 4 Annex 15).

Confirmed: the FDA guidance title, January 2011 date and three stages (process design, process qualification, continued process verification; stage descriptions via an FDA site search because the PDF could not be read directly); Annex 15 titled Qualification and validation, in operation since 1 October 2015 (European Commission page). Removed as unconfirmed: the ASTM E2500 and ISPE baseline references and the claim of usually several consecutive PPQ batches.

Method: documentation only; no commands were run.
