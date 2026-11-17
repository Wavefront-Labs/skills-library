---
id: health-medicine.medical-and-clinical-administration.practice-management-systems.front-desk-to-clean-claim-workflow
name: front-desk-to-clean-claim-workflow
category: health-medicine
field: medical-and-clinical-administration
product: practice-management-systems
tags: [practice-management-systems, medical-and-clinical-administration, practice-management, pms, epic-cadence, epic-resolute, athenahealth, eclinicalworks, nextgen, kareo, tebra, scheduling, patient-registration, eligibility-verification, 270-271, charge-capture, claim-scrubber, clearinghouse, revenue-cycle, work-queues, ar-aging]
level: practitioner
status: docs-checked
description: "Vendor-neutral practice-management system workflow: template scheduling, registration and eligibility (270/271), charge capture, scrubber/clearinghouse edits, work-queues and A/R aging checks."
sources: ["https://www.ecfr.gov/current/title-45/section-162.1102", "https://www.ecfr.gov/current/title-45/section-162.1202", "https://www.cms.gov/files/document/telehealth-faq-updated-10-09-2026.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Front desk to clean claim: a practice-management system workflow

> General clinical/professional reference, not a substitute for independent clinical judgement, current guidelines, or verified dosing references.

**Goal:** configure and run a clinic's practice-management system (PMS) so every visit
flows from booking to a paid claim with as few touches as possible — and know which
screen or report to open when it doesn't.

This is vendor-neutral. Menu names differ (Epic Cadence/Prelude/Resolute,
athenaCollector, eClinicalWorks PM, NextGen PM, Tebra/Kareo); the objects are the same.
Specific menu paths are not given because they vary by version and local build.

## 1. Master files (set up once, audit quarterly)
- **Providers:** NPI, taxonomy code, billing vs rendering relationships, payer
  enrolment/credentialing dates (claims before an effective date deny).
- **Locations/place-of-service codes** (e.g. 22 on-campus outpatient hospital; 02 telehealth other than in the patient's home;
  10 telehealth in the patient's home; Medicare telehealth claims use 02 or 10 with modifier 95 for
  audio-video or 93 for audio-only).
- **Payer table:** payer IDs for the clearinghouse, claim form type, timely-filing
  limits, auth requirements.
- **Fee schedule and charge master:** CPT/HCPCS with fees ≥ highest contracted rate.
- **Appointment types and templates:** visit length, allowed providers, pre-visit
  requirements (e.g. new-patient packet, auth check flag).

## 2. Scheduling
- Build templates from capacity rules (new vs follow-up slots, procedure blocks).
- Book with the correct visit type — it drives duration, reminders and sometimes
  default charges.
- Track no-shows; use automated reminders (SMS/email) and a waitlist for backfill.

## 3. Registration and eligibility (where most denials start)
- Capture demographics exactly as on the insurance card (name, DOB, member ID, group),
  subscriber relationship and coordination-of-benefits order.
- Run **real-time eligibility (270 request → 271 response)** 1–3 days before the visit
  and again on arrival for high-cost services. Read active coverage, plan dates,
  copay/deductible remaining, PCP/referral requirement and carve-outs (e.g. behavioural
  health managed separately).
- Scan card front/back and ID; collect copay and any prior balance at check-in.
- Prior auth needed? Attach the auth number to the visit before it happens.

## 4. Charge capture
- Provider closes the encounter with CPT/HCPCS, modifiers and linked ICD-10 codes;
  charges flow to the PMS. Set a charge-lag target in your policy.
- Reconcile daily: scheduled/arrived visits vs charges posted — the "missing charges"
  report catches unbilled encounters.

## 5. Claim creation and scrubbing
- Claims batch from charges (837P professional / 837I institutional).
- **Scrubber edits** (internal + clearinghouse): missing NPI, invalid diagnosis pointer,
  NCCI bundling conflicts, LCD diagnosis requirements, age/sex conflicts.
- The clearinghouse returns syntax and claim-acknowledgement responses showing accepted and
  rejected claims — work rejections the same day; rejected claims are not on file with the payer.

## 6. Payment posting and work-queues
- Auto-post 835 ERAs; manually post paper EOBs; reconcile deposits to bank.
- Route denials and underpayments into **work-queues** by type (eligibility,
  coding, auth, timely filing) with owners and due dates.
- Patient statements after insurance adjudication; payment plans per policy.

## 7. Reports to watch weekly
- **A/R aging** buckets (0–30, 31–60, 61–90, 91–120, 120+); days in A/R (set the target from a named
  benchmark such as HFMA MAP Keys or MGMA data for your specialty).
- Clean-claim/first-pass rate, denial rate by reason, charge lag, no-show rate,
  point-of-service collections.

## Gotchas
- Editing a demographic after the claim is built doesn't always update the claim —
  rebuild or correct per vendor instructions.
- Duplicate patient records split history and cause duplicate claims; search before
  creating, merge through HIM.
- Credentialing gaps for new providers are invisible until claims deny weeks later.
- Role-based access: front-desk users should not edit fee schedules or write off balances.

## Verify
- [ ] Master files audited (provider enrolment dates, payer IDs, fees).
- [ ] Eligibility run and documented for every scheduled visit.
- [ ] Daily visit-to-charge reconciliation with no unexplained gaps.
- [ ] Clearinghouse rejections worked same day.
- [ ] A/R aging and denial reports reviewed weekly with actions assigned.

## Checked

- Date checked: 2026-10-25. Jurisdiction: United States (HIPAA transactions, CMS place-of-service codes).
- Sources read: eCFR 45 CFR 162.1102 and 162.1202; CMS place-of-service and telehealth FAQ pages (search summaries).
- Confirmed: 837P (005010X222) and 837I (005010X223) as the adopted claim standards; 270/271 (005010X279) for eligibility; POS 02, 10 and 22 definitions; Medicare telehealth POS 02/10 with modifier 93 or 95.
- Corrected or removed: Removed POS 11 example, the 999/277CA names, the charge-lag and days-in-A/R numeric targets (not confirmed).
- Gated: Nothing gated.

Method: documentation only; no commands were run.
