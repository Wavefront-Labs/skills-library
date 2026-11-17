---
id: health-medicine.clinical-research-operations.clinical-trial-site-monitoring.risk-based-monitoring-visit-and-sdv
name: risk-based-monitoring-visit-and-sdv
category: health-medicine
field: clinical-research-operations
product: clinical-trial-site-monitoring
tags: [clinical-trial-site-monitoring, clinical-research-operations, cra, clinical-research-associate, monitoring-visit, risk-based-monitoring, rbm, rbqm, source-data-verification, sdv, source-data-review, sdr, centralized-monitoring, key-risk-indicators, site-initiation-visit, monitoring-visit-report, ich-e6-r3, ich-e8-r1, critical-to-quality, investigator-site-file, issue-escalation, 21-cfr-312]
level: practitioner
status: verified
description: "Run a risk-based CRA monitoring visit: pre-visit KRI review, targeted SDV/SDR, IP and ISF checks, issue grading and escalation, and a follow-up letter within agreed timelines."
sources:
  - "ICH E6(R3) Guideline for Good Clinical Practice (Step 4, January 2025)"
  - "ICH E8(R1) General Considerations for Clinical Studies (2021)"
  - "FDA Guidance: A Risk-Based Approach to Monitoring of Clinical Investigations — Questions and Answers (final, April 2023)"
  - "EMA Reflection Paper on Risk Based Quality Management in Clinical Trials (2013)"
  - "21 CFR Part 312 Subpart D (sponsor and investigator responsibilities)"
  - "Woodin, The CRA's Guide to Monitoring Clinical Research (CenterWatch)"
  - "Regulation (EU) No 536/2014 on clinical trials on medicinal products for human use"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Risk-based monitoring visit and source-data verification

*General clinical/professional reference, not a substitute for independent clinical judgement, current guidelines, or verified dosing references.*

**Goal:** leave every on-site or remote monitoring visit with (a) the critical data and
processes for this site checked to the depth the monitoring plan requires, (b) every issue
graded, owned and dated, and (c) a report and follow-up letter that would stand up at
inspection.

## 1. Know the plan before the site
- Read the **monitoring plan** and risk assessment: which data/processes are
  **critical-to-quality** (ICH E8(R1); E6(R3) proportionality) — typically consent,
  eligibility, primary endpoint, SAEs, IP dosing and blinding.
- The plan sets SDV depth: e.g. 100% SDV of consent, eligibility and SAEs; targeted or
  sampled SDV elsewhere (percentages are sponsor-specific — follow the plan, do not invent).
- Visit frequency is driven by risk and enrolment, not a fixed calendar; early visits after
  first participant in are usual.

## 2. Pre-visit preparation (remote, 1-3 days before)
- Review **centralized-monitoring / KRI** outputs: query age, AE rate vs study mean,
  deviation rate, screen-failure ratio, data-entry lag (e.g. >5 working days), missed visits.
- Pull open action items from the last report; list which participants and visits you will
  verify and why.
- Send a **confirmation letter** with agenda, participants, required staff and EMR access.

## 3. Visit conduct
| Area | What to check |
|---|---|
| Consent | Current IRB/EC-approved version, signed/dated before any procedure, re-consent done, process note present |
| Eligibility | Each inclusion/exclusion criterion traceable to source; investigator sign-off before randomisation |
| SDV / SDR | CRF vs source for critical fields; SDR for plausibility, unreported AEs, con-meds in notes |
| Safety | AEs in notes captured in EDC; SAEs reported to sponsor within the required window (EU CTR Art 41(2): without undue delay, not later than 24 h unless the protocol says otherwise; US 312.64(b): immediately) |
| IP | Accountability log vs physical stock, temperature logs and excursions, blinding integrity |
| ISF/essential records | Delegation log matches who did what; CVs/training/GCP current; lab certs and ranges |
| Facilities | Equipment calibration, sample storage and shipping |

Use **ALCOA+** (attributable, legible, contemporaneous, original, accurate, complete,
consistent, enduring, available) as the lens for source quality.

## 4. Grade and escalate
- Grade findings: **critical** (participant safety/rights or data reliability at risk,
  e.g. no consent, ineligible participant dosed), **major**, **minor** (sponsor SOP terms vary).
- Critical issues: tell the PI before you leave and escalate to the study manager the same
  day; possible **serious breaches** in the EU must reach the sponsor fast enough to meet the
  Art 52 clock: the sponsor notifies Member States without undue delay and not later than 7 days after becoming aware (a serious breach is likely to affect significantly subject safety/rights or data reliability).
- Persistent non-compliance → the sponsor must promptly secure compliance or stop shipments of the drug to the investigator and end their participation (21 CFR 312.56(b)); apply ICH E6(R3) and the sponsor SOP for further steps.

## 5. Close-out of the visit
- Exit meeting with PI/coordinator: findings, actions, owners, dates.
- **Monitoring visit report** within the SOP window (commonly 5-10 working days) and a
  **follow-up letter** to the site; file both in TMF/ISF.
- Track actions in CTMS until verified closed at the next contact.

## Gotchas
- 100% SDV is not quality: transcription checks miss unreported AEs that SDR of clinic notes finds.
- Do not "fix" source or coach entries; write queries and let the site correct with audit trail.
- Remote SDV needs controlled, read-only EMR access with privacy safeguards (verify local law).
- A clean CRF with no AEs in a sick population is a signal, not a success.
- Undocumented verbal agreements with the site do not exist at inspection.

## Verify
- [ ] Visit scope traced to the monitoring plan and KRI review.
- [ ] Consent, eligibility and SAE checks completed for all in-scope participants.
- [ ] Every finding graded with owner and due date in CTMS.
- [ ] Critical issues escalated same day and documented.
- [ ] Report and follow-up letter issued within SOP timelines and filed.
