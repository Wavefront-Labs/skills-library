---
id: health-medicine.clinical-research-operations.gcp-and-protocol-compliance.protocol-deviation-handling-and-capa
name: protocol-deviation-handling-and-capa
category: health-medicine
field: clinical-research-operations
product: gcp-and-protocol-compliance
tags: [gcp-and-protocol-compliance, clinical-research-operations, good-clinical-practice, gcp, protocol-deviation, important-protocol-deviation, serious-breach, eu-ctr-article-52, capa, root-cause-analysis, five-whys, fishbone, essential-records, trial-master-file, tmf, investigator-site-file, inspection-readiness, audit, fda-483, bimo, ich-e6-r3, ich-e3, 21-cfr-312]
level: practitioner
status: verified
description: "Identify, classify and report protocol deviations and serious breaches (ICH E6(R3), EU CTR Art 52), run root-cause analysis and CAPA, and keep the TMF inspection-ready."
sources:
  - "ICH E6(R3) Guideline for Good Clinical Practice (Step 4, January 2025)"
  - "ICH E3 Structure and Content of Clinical Study Reports, and E3 Q&A (R1) on protocol deviations"
  - "Regulation (EU) No 536/2014, Article 52 (serious breach) and Article 58 (archiving)"
  - "EMA Guideline for the notification of serious breaches of Regulation (EU) No 536/2014 or the clinical trial protocol"
  - "FDA Draft Guidance: Protocol Deviations for Clinical Investigations of Drugs, Biological Products, and Devices (December 2024)"
  - "FDA Compliance Program Guidance Manual 7348.811 (Clinical Investigators and Sponsor-Investigators)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Protocol deviation handling and CAPA

*General clinical/professional reference, not a substitute for independent clinical judgement, current guidelines, or verified dosing references.*

**Goal:** every departure from the protocol or GCP is caught, classified correctly, reported
on time to the right party, fixed at its root, and visible in the records an inspector will
read.

## 1. Identify
Sources: monitoring visits, EDC edit checks and listings, IRT/IP logs, central-monitoring
KRIs, site self-report, audits. Typical deviations: out-of-window visits, missed
assessments, wrong consent version, eligibility violations, dosing errors, unblinding,
temperature-excursion product used.

## 2. Classify
| Class | Definition (paraphrased) | Examples |
|---|---|---|
| **Important** (ICH E6(R3): important deviations are a subset of protocol deviations; FDA draft guidance uses the same term) | May significantly affect completeness, accuracy or reliability of key data, or participant rights, safety or well-being | Ineligible participant randomised; no consent; primary endpoint not collected; wrong IP dose |
| Non-important | Does not meet the above | Visit 1 day out of window for a non-critical assessment |
| **Serious breach** (EU CTR Art 52) | Likely to affect to a significant degree the safety and rights of a subject or the reliability and robustness of data | Systematic falsification; repeated dosing errors; widespread consent failures |

Classification criteria should be pre-specified in a deviation plan; apply them, do not
re-argue each case.

## 3. Report
- **Site → sponsor:** per protocol (often within days; immediately if safety-related).
- **Site → IRB/EC:** per IRB policy — many US IRBs want only deviations affecting
  safety/rights/data promptly; EU ECs vary by member state (verify).
- **Sponsor → EU authorities:** serious breach via the EU portal (CTIS) without undue delay and **not later than 7 days** after becoming aware (CTR Art 52(1)).
- **US:** no general FDA deviation report; important deviations go in the CSR and
  appear at BIMO inspection. Deviations to eliminate immediate hazard may be implemented
  before IRB approval, then reported (21 CFR 56.108(a)(4); 312.30(b)(2)(ii): a protocol change to eliminate an apparent immediate hazard may be made immediately, with FDA notified by protocol amendment and the IRB notified per 56.104(c)).
- Log every deviation (participant, date, description, class, report dates) in CTMS/EDC.

## 4. Root cause and CAPA
1. Contain: protect participants first (e.g. stop dosing, re-consent, quarantine IP).
2. Root cause: **5 Whys** or **fishbone** (people, process, protocol design, systems,
   environment). "Human error" is a starting point, not a root cause.
3. **Corrective action** fixes this instance; **preventive action** stops recurrence
   (checklist change, IRT hard-stop, protocol clarification letter, amendment).
4. SMART actions: owner, due date, and an **effectiveness check** (e.g. zero recurrence
   in next 20 visits or 3 months — choose a measurable metric).
5. Trend deviations across sites; repeated categories point to protocol design faults.

## 5. Inspection readiness
- TMF/ISF current against the **TMF Reference Model** index; contemporaneous filing.
- Essential records per ICH E6(R3) Appendix C: approvals, delegation log, CVs/GCP training,
  consent forms, IP records, monitoring reports, deviation log, safety reports.
- Retention: EU CTR Art 58 — at least 25 years after the trial ends (subjects' medical files per national law); US 21 CFR 312.62(c) — 2 years after approval of the application for the indication, or, if none, 2 years after discontinuation and FDA notification (sponsors often require longer).
- Storyboards for known major issues: what happened, impact, CAPA, evidence of effectiveness.

## Gotchas
- Waivers/"protocol exemptions" granted in advance to enrol ineligible participants are not acceptable GCP.
- Late reclassification (to non-important) near lock looks like data cleaning by definition.
- A CAPA without an effectiveness check is unclosed.
- Respond to a Form 483 in writing with a corrective action plan and implement it promptly; FDA considers responses when deciding further action (FDA 483 FAQ). Check the response deadline stated in FDA's own letters, not a remembered figure.

## Verify
- [ ] Deviation logged with class per pre-specified criteria.
- [ ] Reports made within sponsor, IRB/EC and (EU) 7-day serious-breach timelines.
- [ ] Root cause documented beyond "human error".
- [ ] CAPA has owner, date and effectiveness metric.
- [ ] TMF/ISF reflects the deviation, reports and CAPA closure.
