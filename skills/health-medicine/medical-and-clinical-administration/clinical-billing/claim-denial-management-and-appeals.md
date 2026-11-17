---
id: health-medicine.medical-and-clinical-administration.clinical-billing.claim-denial-management-and-appeals
name: claim-denial-management-and-appeals
category: health-medicine
field: medical-and-clinical-administration
product: clinical-billing
tags: [clinical-billing, medical-and-clinical-administration, denial-management, claim-appeals, carc, rarc, era, 835, 837, remittance-advice, claim-scrubbing, timely-filing, revenue-cycle, medical-billing, root-cause-analysis, clean-claim-rate, ub-04, cms-1500]
level: practitioner
status: docs-checked
description: "Working claim denials: read the 835/EOB reason codes, triage correctable vs appealable, fix-and-resubmit vs written appeal, track root causes, and prevent repeats upstream."
sources: ["https://x12.org/codes/claim-adjustment-reason-codes", "https://www.ecfr.gov/current/title-42/section-405.942"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Claim denial management and appeals

> General clinical/professional reference, not a substitute for independent clinical judgement, current guidelines, or verified dosing references.

**Goal:** recover legitimately owed payment on every denied claim before deadlines, and
feed each denial's root cause back upstream so the same denial stops happening.

Context: US-centric terminology (837 claims, 835 remittances, CARC/RARC codes,
Medicare redetermination). Payer contracts and state rules override generic advice.

## 1. Read the denial precisely
From the 835 electronic remittance (or paper EOB/RA) capture per line:
- **Group code:** CO (contractual obligation), PR (patient
  responsibility), OA (other adjustment), PI (payer-initiated reduction).
- **CARC** (why) and **RARC** (detail). Examples: CARC 16 = missing/invalid info;
  CARC 50 = not medically necessary; CARC 97 = bundled into another service;
  CARC 29 = timely filing expired; CARC 197 = precertification/authorization absent;
  CARC 18 = exact duplicate (X12 limits it to group code OA except where state workers'
  compensation rules require CO). Look up the current list — codes are added and retired
  (CARC 15 and 57 are deactivated).
- Denied vs **rejected**: rejections fail front-end edits and never entered
  adjudication; they're fixed and resubmitted as a new claim, not appealed.

## 2. Triage into buckets
| Bucket | Typical CARCs | Action |
|---|---|---|
| Correctable data errors | 16, 31 (patient not identified), 109 (wrong payer) | Correct and submit a corrected (replacement) claim per the payer's rules |
| Eligibility/coverage | 27 (coverage ended), 109 | Verify coverage; bill correct payer or patient |
| Authorization | 197 | Check if auth existed; retro-auth request or appeal with proof |
| Coding/bundling | 97, 4 (modifier), 11 (dx inconsistent) | Coder review; a modifier only if documentation supports it |
| Medical necessity | 50 | Clinical appeal with documentation and policy criteria |
| Timely filing | 29 | Appeal only with proof of timely original submission |
| Duplicate | 18 | Check if original paid; otherwise appeal with distinction |
Prioritise by dollar value × deadline proximity.

## 3. Write an appeal that wins
- Use the payer's form/portal where required; quote claim number, patient ID, DOS,
  denied lines and CARC/RARC.
- **One argument per denial reason**, tied to evidence: the medical record excerpt,
  the payer's own coverage policy criteria (cite policy number and the criteria met),
  authorization number, proof of timely filing (clearinghouse acceptance report).
- Request a specific remedy ("reprocess line 2 for payment per contract rate").
- Note appeal levels and deadlines. For Medicare Part A/B: redetermination within 120
  calendar days of receiving the notice of the initial determination (receipt is presumed 5
  calendar days after the notice date), then the next appeal level; commercial payers
  set their own windows — verify per contract.
- For clinical denials, offer or request a **peer-to-peer** discussion between the
  treating physician and the payer's medical director.

## 4. Track and prevent
- Log every denial: payer, CARC, service line, department, root cause, recoverable?,
  outcome, days to resolution.
- Monthly: denial rate (by count and value), top 10 CARCs, overturn rate, write-offs.
  Set targets against a named benchmark source (e.g. HFMA MAP Keys) and your payer mix.
- Push fixes upstream: registration scripts for eligibility, auth work-queues before
  scheduling, scrubber edits for recurring coding errors, documentation education.

## Gotchas
- Never resubmit a denied claim as a new original (duplicate denial) — use corrected
  claim or appeal per payer rules.
- Never add a modifier just to bypass an edit; that is a compliance (false claims) risk.
- Contractual adjustments (CO-45) are not denials — don't appeal them unless the
  allowed amount violates the contract.
- Balance-billing the patient for CO-group adjustments is generally not allowed; check the payer contract.

## Verify
- [ ] Each denial categorised by group code, CARC and RARC.
- [ ] Rejections and denials routed to the correct workflow.
- [ ] Appeals cite evidence and policy, request a specific remedy, and meet deadlines.
- [ ] Denial log updated with root cause and outcome.
- [ ] At least one upstream prevention action assigned for top recurring causes.

## Checked

- Date checked: 2026-10-25. Jurisdiction: United States (X12 CARC/RARC, Medicare appeals).
- Sources read: X12 CARC list (read 2026-10-25); 42 CFR 405.942 on eCFR.
- Confirmed: Descriptions of CARC 4, 11, 16, 18, 27, 29, 31, 45, 50, 97, 109 and 197; group code names; the 120-calendar-day redetermination limit and 5-day receipt presumption.
- Corrected or removed: CARC 15 and CARC 57 are deactivated (stop dates 2018-05-01 and 2007-06-30), so they were removed from the triage table; CARC 18 is restricted to group code OA; the redetermination clock runs from receipt of the notice, not from the determination; unsupported benchmark figures, appeal-window ranges and form-code details were removed.
- Gated: Nothing gated.

Method: documentation only; no commands were run.
