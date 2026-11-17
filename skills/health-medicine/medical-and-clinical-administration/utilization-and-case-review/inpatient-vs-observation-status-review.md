---
id: health-medicine.medical-and-clinical-administration.utilization-and-case-review.inpatient-vs-observation-status-review
name: inpatient-vs-observation-status-review
category: health-medicine
field: medical-and-clinical-administration
product: utilization-and-case-review
tags: [utilization-and-case-review, medical-and-clinical-administration, utilization-review, admission-status, observation-status, two-midnight-rule, inpatient-only-list, condition-code-44, moon-notice, physician-advisor, length-of-stay, avoidable-days, discharge-barriers, case-management, interqual, mcg, medicare]
level: practitioner
status: gated
description: "Hospital admission-status review: apply the Medicare two-midnight rule and commercial criteria, escalate to a physician advisor, handle Condition Code 44 and MOON notices, and track avoidable days."
sources: ["https://www.ecfr.gov/current/title-42/section-412.3", "https://www.ecfr.gov/current/title-42/section-422.101", "https://www.ecfr.gov/current/title-42/section-489.20", "https://www.ecfr.gov/current/title-42/section-405.1205", "https://www.cms.gov/newsroom/fact-sheets/medicare-outpatient-observation-notice-moon"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Inpatient vs observation status review

> General clinical/professional reference, not a substitute for independent clinical judgement, current guidelines, or verified dosing references.

**Goal:** make sure every hospitalised patient's status (inpatient vs outpatient
observation) is correct, supported by documentation and communicated to the patient —
early enough to change it without rebilling chaos.

Context: US hospitals. Status affects Medicare Part A vs B billing, patient cost
sharing and skilled-nursing-facility eligibility (three-day *inpatient* stay rule).

## 1. Review timing
Screen every admission and every observation patient **within 24 hours** (ideally
before the order is final for ED admissions), then at least daily for observation
patients and at key changes (e.g. procedure, deterioration).

## 2. Apply the right rule set
**Traditional Medicare and (since 2024) Medicare Advantage — two-midnight rule:**
- Inpatient is generally appropriate when the admitting practitioner **expects** the
  patient to need medically necessary hospital care spanning **≥ 2 midnights**, and
  documents the reasons (time in ED/observation before the order counts toward the
  expectation, but the inpatient stay begins with the order (gated: unconfirmed, source is paywalled or blocked)).
- **Inpatient-only list** procedures are inpatient regardless of expected LOS.
- Expectation < 2 midnights → usually outpatient/observation, *unless* case-by-case
  exception supported by documented complex medical factors (risk, comorbidity,
  severity).
- An unexpected early recovery, death or AMA departure does not invalidate a
  reasonable expectation that was documented (gated: unconfirmed, source is paywalled or blocked).

**Commercial / Medicaid managed care:** apply the contract's criteria (often InterQual
or MCG severity-of-illness/intensity-of-service screens) and authorization rules.

## 3. When the screen fails → physician advisor
Nurse reviewers flag; they don't change orders. Escalate to a **physician advisor**
(second-level review), who reviews the record and may speak with the attending. The
attending writes any status-change order.

## 4. Changing status
- **Inpatient → outpatient (Condition Code 44):** allowed for Medicare only if
  (1) change happens before discharge (gated: unconfirmed, source is paywalled or blocked), (2) the hospital hasn't submitted a Part A claim,
  (3) the UR committee concurs, and (4) the practitioner responsible for the patient's care
  concurs and the concurrence is documented in the record. The patient must be notified (gated: unconfirmed, source is paywalled or blocked).
  Afterwards, bill as outpatient.
- If the Condition Code 44 conditions are not met, the hospital may bill covered Part B-only
  services on a 12x bill type — slower and lower paying.
- **Outpatient → inpatient:** a new order; inpatient starts at the order time.

## 5. Notify the patient
- **MOON** (Medicare Outpatient Observation Notice): to Medicare beneficiaries (including Medicare Advantage
  enrollees) receiving observation services as outpatients for more than 24 hours, **no later
  than 36 hours** after observation starts (sooner if transferred, discharged or admitted; it may
  be given before 24 hours), with an oral explanation and the beneficiary's signature (42 CFR 489.20).
- **Important Message from Medicare (IM)** (the standardized notice of hospital inpatient
  rights): no later than 2 calendar days after admission, plus a follow-up copy before discharge, no
  more than 2 calendar days before discharge (42 CFR 405.1205).

## 6. Length-of-stay and avoidable days
Once status is settled, review daily for continued stay need and **discharge barriers**
(awaiting placement, test scheduling, consult delay, insurance auth for post-acute
care). Log avoidable days by cause and escalate systemic ones (e.g. weekend MRI
access) to operations.

## Gotchas
- "Admit to inpatient — telemetry" with no rationale for the expected stay is the most
  common documentation gap; ask for the reason, not just the order.
- Observation hours: count from the observation order, exclude time for separately
  billable procedures; time in ED before the order is not observation (gated: unconfirmed, source is paywalled or blocked).
- SNF three-day rule counts inpatient midnights only (gated: unconfirmed, source is paywalled or blocked) — status errors can cost patients
  thousands.
- Condition Code 44 cannot be used after discharge.

## Verify
- [ ] Each admission reviewed within 24 h using the correct payer rule set.
- [ ] Failed screens escalated to a physician advisor, not changed by reviewers.
- [ ] Status changes meet all Condition Code 44 conditions and are documented.
- [ ] MOON and IM notices delivered on time and recorded.
- [ ] Avoidable days logged with a cause and owner.

## Checked

- Date checked: 2026-10-25. Jurisdiction: United States (Medicare Part A/B and Medicare Advantage).
- Sources read: eCFR 42 CFR 412.3, 422.101, 405.1205 (read); 42 CFR 489.20 and CMS MOON fact sheet (search summary; the CMS MOON page URL tried returned 404); CMS Claims Processing Manual Ch. 1 s50.3 (search summary).
- Confirmed: Two-midnight expectation, case-by-case exception and inpatient-only wording in 412.3(d); MA plans must follow 412.3 payment criteria (422.101(b)(2)); MOON for more than 24 hours of outpatient observation, due within 36 hours, oral and written, for Original Medicare and MA enrollees; IM within 2 calendar days of admission with a follow-up copy; Condition Code 44 needs practitioner and UR committee concurrence documented in the record and the claim not yet submitted; Part B-only 12x bill type when conditions are not met.
- Corrected or removed: MOON and IM wording corrected and made specific; the "self-denied and rebilled under Part B" sentence replaced with the 12x bill type wording; the physician-only UR concurrence was replaced by the manual wording.
- Gated: Timing of the inpatient order, the "before discharge" condition for CC44, the patient-notification requirement, the observation-hours counting rule and the SNF three-day rule: the CMS manual PDFs returned binary text.

Method: documentation only; no commands were run.
