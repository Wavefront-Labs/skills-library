---
id: health-medicine.medical-and-clinical-administration.insurance-claims-review.medical-necessity-and-prior-authorization-review
name: medical-necessity-and-prior-authorization-review
category: health-medicine
field: medical-and-clinical-administration
product: insurance-claims-review
tags: [insurance-claims-review, medical-and-clinical-administration, medical-necessity, prior-authorization, utilization-review, coverage-determination, interqual, mcg, milliman, ncd, lcd, peer-to-peer, adverse-determination, nurse-reviewer, physician-reviewer, payer, urac]
level: practitioner
status: docs-checked
description: "Payer-side medical-necessity and prior-auth review: confirm benefit, apply the right criteria (NCD/LCD, InterQual, MCG, policy), document each criterion and escalate denials to a physician."
sources: ["https://www.cms.gov/newsroom/fact-sheets/cms-interoperability-prior-authorization-final-rule-cms-0057-f", "https://www.ecfr.gov/current/title-42/section-422.101", "https://www.ecfr.gov/current/title-42/section-422.566"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Medical-necessity and prior-authorization review

> General clinical/professional reference, not a substitute for independent clinical judgement, current guidelines, or verified dosing references.

**Goal:** reach a defensible, timely coverage determination by applying the correct
criteria to the actual clinical record — and route anything you can't approve to a
qualified physician reviewer rather than denying it yourself.

Context: US payer/utilization-management practice. Turnaround clocks and reviewer
qualifications are set by federal rules (Medicare Advantage, Medicaid), state law,
ERISA and accreditation (URAC/NCQA) — check which apply to the plan.

## 1. Intake checks (non-clinical)
- Member eligible on the date of service; the service is a **covered benefit** under
  this plan (a benefit exclusion is not a medical-necessity denial — different notice
  and appeal rights).
- Request complete: CPT/HCPCS, ICD-10 codes, site of service, units, requesting and
  rendering provider, clinical notes.
- Urgency: under CMS-0057-F, impacted payers (including Medicare Advantage, state Medicaid
  and CHIP programs; excluding drugs and QHP issuers on the federally-facilitated exchanges)
  must decide expedited requests within 72 hours and standard requests within 7 calendar days,
  from 1 January 2026. Other programs and state law differ. Start the clock at receipt.
- Missing information → pend and request specific items with a deadline; don't deny
  for "insufficient information" without a documented request.

## 2. Choose the criteria hierarchy
Apply in the order the plan specifies, typically:
1. Statute/regulation and plan contract.
2. **Medicare:** National Coverage Determination (NCD) → Local Coverage Determination
   (LCD) / Article for the MAC jurisdiction. Medicare Advantage plans must follow these
   and may only use internal criteria when Medicare criteria are not fully established.
3. Plan medical/pharmacy policy (cite number and version date).
4. Licensed screening criteria (InterQual, MCG) — screening tools, not final arbiters.

## 3. Review the clinical record against criteria
- Walk each criterion and mark **met / not met / not documented**, citing the source
  document and date (e.g. "Conservative therapy ≥ 6 weeks: met — PT notes 2 Mar–20 Apr").
- Typical criteria themes: diagnosis confirmed by appropriate testing; failure or
  contraindication of first-line therapy (step therapy); severity thresholds; provider
  specialty; site-of-service appropriateness.
- Consider individual circumstances: comorbidities, contraindications, and whether the
  criteria fit the clinical scenario at all.

## 4. Decide and document
- **All criteria met → approve** (nurse reviewers can usually approve).
- **Not met or unclear → refer to a physician (or appropriate clinical peer) reviewer.**
  For Medicare Advantage a clinician with relevant expertise must review before a
  medical-necessity denial (42 CFR 422.566(d)); other programs and state law set their own
  reviewer rules. Offer the requesting provider a **peer-to-peer** discussion.
- Determination note: request summary, criteria version applied, criterion-by-criterion
  findings, rationale in plain language, reviewer credentials, timestamps.
- Adverse determination letters should state (requirements vary by program) the specific reason, the criteria used (and
  how to obtain them), alternative covered options if any, and appeal rights/deadlines.

## 5. Quality loop
Track turnaround compliance, overturn rate on appeal (a high overturn rate signals
criteria misapplication), inter-rater reliability audits, and requests that should be
removed from prior-auth lists because they're almost always approved ("gold carding").

## Gotchas
- Screening criteria not met ≠ not medically necessary; it means "escalate".
- Applying commercial policy to a Medicare Advantage member when an NCD/LCD exists.
- Retrospective review using information not available to the treating clinician at
  the time.
- Clock violations can bring regulatory or contractual consequences.
- Never let financial considerations appear in clinical rationale.

## Verify
- [ ] Eligibility, benefit and urgency established; clock started.
- [ ] Correct criteria hierarchy and version identified and cited.
- [ ] Each criterion marked with source evidence.
- [ ] Any non-approval reviewed by a qualified physician/peer; P2P offered.
- [ ] Determination and notice contain reason, criteria and appeal rights, within deadline.

## Checked

- Date checked: 2026-10-25. Jurisdiction: United States (Medicare Advantage, Medicaid, CHIP; commercial plans vary).
- Sources read: CMS-0057-F fact sheet (via search summary; the PDF URL tried returned 404); eCFR 42 CFR 422.101 and 422.566.
- Confirmed: Decision timeframes (72 hours expedited, 7 calendar days standard, from 1 Jan 2026) and their exclusions; NCD/LCD compliance and the limit on internal coverage criteria (422.101(b)(1)-(3), (b)(6)); clinician review before a medical-necessity denial (422.566(d)).
- Corrected or removed: Replaced the vague timeframe sentence with the rule text and exclusions; replaced the "only a physician" claim with the MA reviewer rule; removed the unsupported "deemed approval" consequence.
- Gated: Nothing gated.

Method: documentation only; no commands were run.
