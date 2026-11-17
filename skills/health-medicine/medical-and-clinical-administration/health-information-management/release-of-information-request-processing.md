---
id: health-medicine.medical-and-clinical-administration.health-information-management.release-of-information-request-processing
name: release-of-information-request-processing
category: health-medicine
field: medical-and-clinical-administration
product: health-information-management
tags: [health-information-management, medical-and-clinical-administration, release-of-information, roi, hipaa, right-of-access, minimum-necessary, authorization, 42-cfr-part-2, psychotherapy-notes, subpoena, designated-record-set, accounting-of-disclosures, gdpr-subject-access, him, rhia, rhit, information-blocking]
level: practitioner
status: docs-checked
description: "Process release-of-information requests: classify requester, verify identity and authority, check authorization validity, apply special-protection rules, release minimum necessary, log the disclosure."
sources: ["https://www.ecfr.gov/current/title-45/part-164/subpart-E", "https://www.hhs.gov/hipaa/for-professionals/regulatory-initiatives/fact-sheet-42-cfr-part-2-final-rule/index.html", "https://www.ecfr.gov/current/title-45/part-171"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Release-of-information request processing

> General clinical/professional reference, not a substitute for independent clinical judgement, current guidelines, or verified dosing references.

**Goal:** release exactly the right records to exactly the right person, on time, with
an audit trail — and never release protected information without its specific legal
basis. This is not legal advice; route anything unusual to privacy/legal counsel.

Context: US HIPAA framework. Other jurisdictions apply a similar workflow with different
time limits and grounds; check local law.

## 1. Classify the request
| Requester | Legal basis | Typical handling |
|---|---|---|
| Patient (or personal representative) | **Right of access** (164.524) | No authorization form needed beyond a written request; respond within 30 days (one 30-day extension with notice); fee limited to reasonable cost-based |
| Provider for treatment | Treatment disclosure (164.506) | No authorization; still verify the requester |
| Payer for payment / operations | 164.506 | Minimum necessary applies |
| Third party (lawyer, insurer, employer) | **Valid authorization** (164.508) | Check every required element |
| Court order | 164.512(e) | Release as ordered |
| Subpoena without court order | 164.512(e) | Needs satisfactory assurance (notice to patient or qualified protective order); involve legal |
| Public health, law enforcement, coroner | 164.512 specific provisions | Follow the specific paragraph; log |

## 2. Verify identity and authority
- Patient: photo ID or verified portal identity.
- Personal representative: documentation (parent of minor — check state minor-consent
  exceptions; healthcare power of attorney; executor/administrator for a deceased
  patient).
- Organisation: letterhead, callback to a verified number.

## 3. Check a third-party authorization
Required core elements: specific description of information; who may disclose; to
whom; purpose (or "at the request of the individual"); **expiration date or event**;
signature and date (and representative's authority). Required statements: right to
revoke, whether treatment is conditioned on signing, potential for redisclosure.
Missing any element → invalid; return with explanation.

## 4. Apply special protections
- **Psychotherapy notes** (kept separately from the record) need their own specific
  authorization; they're excluded from the right of access.
- **Substance-use disorder records** from a Part 2 programme: Part 2 consent rules and a
  redisclosure notice apply (the 2024 Part 2 final rule took effect 16 April 2024; HHS gives
  16 February 2026 as the compliance date, with the accounting-of-disclosures provision dated separately).
- State-law protections often add rules for HIV, genetic testing, mental health,
  reproductive health and minors' confidential services. Apply the stricter rule.

## 5. Compile and release
- Pull from the **designated record set** only what is requested and permitted;
  apply minimum necessary for non-treatment, non-patient disclosures.
- Patients may request a format (electronic copy, portal, specific app) — provide it if
  readily producible. Unreasonable delay or interference can be **information blocking**
  under the Cures Act.
- Quality check before sending: right patient on every page (two identifiers), no
  misfiled documents from other patients, page count matches.
- Send by secure method; encrypted email/portal for electronic.

## 6. Log
Record date, requester, legal basis, what was sent, method and staff member. Disclosures
outside treatment, payment and operations (and outside authorizations) must be
available for an **accounting of disclosures** (6-year look-back; act on a request within 60 days, one 30-day extension; other exceptions apply under 164.528(a)).

## Gotchas
- A misfiled page from another patient may be a reportable breach (assess under the HIPAA Breach Notification Rule) — the page-by-page check
  is the most important step.
- Denying a patient access because of an unpaid bill is not permitted.
- An expired or undated authorization is invalid even if everything else is perfect.
- Phone requests from "the patient's daughter" are not verified authority.

## Verify
- [ ] Requester classified and legal basis identified.
- [ ] Identity/authority verified and documented.
- [ ] Authorization (if needed) has all core elements and statements.
- [ ] Special-protection records handled per specific rules.
- [ ] Every page checked for correct patient; release logged within the deadline.

## Checked

- Date checked: 2026-10-25. Jurisdiction: United States (HIPAA, 42 CFR Part 2, 45 CFR Part 171).
- Sources read: eCFR 45 CFR 164.524, 164.528, 164.508, 164.512(e), 171.103; HHS Part 2 fact sheet (updated 30 Jan 2026).
- Confirmed: Right of access: 30 days plus one 30-day extension, reasonable cost-based fee, psychotherapy notes excluded, form and format requested if readily producible, no unpaid-bill ground; accounting of disclosures: 6-year look-back; authorization core elements and required statements; subpoena satisfactory-assurance routes (notice or qualified protective order); information-blocking definition; Part 2 compliance date 16 Feb 2026.
- Corrected or removed: Replaced "confirm current compliance dates" with the HHS date; softened the breach statement; removed the GDPR time-limit claim (not checked); added the 60-day accounting response limit.
- Gated: Nothing gated.

Method: documentation only; no commands were run.
