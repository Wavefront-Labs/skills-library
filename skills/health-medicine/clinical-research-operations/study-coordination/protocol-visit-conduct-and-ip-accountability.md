---
id: health-medicine.clinical-research-operations.study-coordination.protocol-visit-conduct-and-ip-accountability
name: protocol-visit-conduct-and-ip-accountability
category: health-medicine
field: clinical-research-operations
product: study-coordination
tags: [study-coordination, clinical-research-operations, clinical-research-coordinator, crc, study-nurse, participant-screening, screening-log, enrolment, visit-window, schedule-of-assessments, source-documentation, alcoa-plus, investigational-product, drug-accountability, ip-dispensing, temperature-excursion, delegation-log, irt, ivrs, ich-e6-r3, 21-cfr-312, protocol-adherence]
level: practitioner
status: verified
description: "Coordinate trial visits at site: screening log, visit-window scheduling, protocol-driven visit checklists, source documentation (ALCOA+) and investigational-product accountability."
sources:
  - "ICH E6(R3) Guideline for Good Clinical Practice (Step 4, January 2025)"
  - "21 CFR 312.60-312.62 (investigator responsibilities, IP control, records)"
  - "Regulation (EU) No 536/2014, Articles 51 and 58 and Annex VI (traceability and labelling of IMP)"
  - "EudraLex Volume 4, Annex 13 / Commission Delegated Regulation (EU) 2017/1569 on GMP for IMPs"
  - "Woodin, The CRC's Guide to Coordinating Clinical Research (CenterWatch)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Protocol visit conduct and investigational-product accountability

*General clinical/professional reference, not a substitute for independent clinical judgement, current guidelines, or verified dosing references.*

**Goal:** every participant visit happens inside its window, every protocol procedure is done
by a delegated person and documented in source, and every unit of investigational product
(IP) can be traced from receipt to return or destruction.

## 1. Screening and enrolment
- Keep a **screening/enrolment log** of everyone pre-screened (de-identified per local
  privacy rules): date, outcome, reason for screen failure.
- No study-specific procedure before **valid consent** (see
  health-medicine.clinical-research-operations.informed-consent-and-participant-protection.informed-consent-process-and-documentation).
- Build an **eligibility checklist** that cites the source for each criterion (lab value
  and date, imaging report, clinic note). The investigator signs and dates it **before**
  randomisation in IRT/IVRS.
- Check criterion time windows (e.g. "eGFR within 14 days of Day 1") against actual dates.

## 2. Scheduling from the schedule of assessments
- Convert the protocol's schedule of assessments into a per-participant calendar keyed to
  the anchor date (usually Day 1/randomisation), with **window** limits (e.g. Day 29 ± 3 days).
- Book the next visit before the participant leaves; flag fasting, washout, PK timing
  (e.g. pre-dose trough within 30 min before dosing) and diary returns.
- Out-of-window visits are deviations — record them; never shift the anchor date to hide them.

## 3. Visit checklist (per visit, versioned to protocol amendment)
| Step | Notes |
|---|---|
| Confirm consent version is current | Re-consent if a new version is approved |
| Interval history: AEs, con-meds, hospitalisations | Ask open questions; record start/stop dates |
| Procedures in protocol order | Vitals before blood draw if specified; ECG rest periods |
| Samples | Lab manual: tubes, spin time, temperature, shipping cut-offs |
| IP dispensing/administration | Per IRT assignment; second-person check where required |
| Source completed | Signed and dated by the person who did it, contemporaneously |
| EDC entry | Within the sponsor's target (often 3-5 working days) |

Source must meet **ALCOA+**. Corrections: single line, initials, date, reason — never obscure
the original. In EMRs, the audit trail does this.

## 4. Investigational-product accountability
- **Receipt:** check shipment vs packing list, temperature monitor, damage; acknowledge in
  IRT; quarantine if an excursion and await sponsor disposition.
- **Storage:** secure, access-limited, continuous temperature logging (min/max daily or
  logger) with calibrated devices.
- **Dispensing log:** participant ID, kit number, quantity, date, by whom.
- **Returns:** count returned units, calculate compliance
  ((dispensed − returned) ÷ expected × 100%; protocol often defines 80-120% as compliant).
- **Reconciliation:** received = dispensed + returned + on hand + destroyed (zero
  unexplained balance). Destruction only with sponsor authorisation and a certificate.
- Records retained per 21 CFR 312.62(c) (2 years after the marketing application is approved for the indication, or if none is filed or approved, 2 years after the investigation is discontinued and FDA is notified) or EU CTR Art 58 (sponsor and investigator archive the TMF content at least 25 years after the trial ends; subjects' medical files per national law). The investigator must keep disposition records of dates, quantity and use by subjects (312.62(a)); the sponsor agreement may require longer.

## 5. Delegation and communication
- Only staff on the **delegation log**, trained on the current protocol, perform tasks.
- Escalate safety events to the investigator immediately; SAEs to sponsor per protocol
  (EU CTR Art 41(2): not later than 24 h after knowledge unless the protocol provides otherwise; US 312.64(b): immediately).

## Gotchas
- Pre-screening using records can need its own ethics approval or waiver (jurisdiction-specific).
- Blinded staff must not see kit-level information that reveals treatment.
- A "transcribed" paper worksheet becomes source if it is the first record — define source
  per study in a source-document agreement.
- Temperature excursion product is not used until the sponsor releases it in writing.

## Verify
- [ ] Eligibility checklist signed by investigator before randomisation.
- [ ] Every visit date within window or a deviation logged.
- [ ] Source attributable and contemporaneous for each procedure.
- [ ] IP reconciliation balances to zero with temperature records complete.
- [ ] Delegation log matches who performed each task.
