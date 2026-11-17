---
id: engineering-technology.biomedical-engineering.device-verification-validation.software-anomaly-management
name: software-anomaly-management
category: engineering-technology
field: biomedical-engineering
product: device-verification-validation
tags: [software-anomaly, software-problem-resolution, defect-triage, iec-62304-problem-resolution, known-anomalies]
level: practitioner
status: draft
description: "Manage software anomalies under IEC 62304: logging, triage by severity and risk, investigation, fix verification, release of known anomalies and regulatory disclosure."
sources: ["IEC 62304 Medical device software - Software life cycle processes (problem resolution process and anomaly list; confirm edition)", "FDA guidance on content of premarket submissions for device software functions (confirm current text)", "https://www.iec.ch"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Software anomaly management

**Goal:** make sure every software problem is recorded, assessed for patient risk, resolved or justified before release.

## Process
1. **Log every anomaly** from development, testing and the field in a tracking system: description, steps, version, environment and evidence.
2. **Triage:** classify by effect on safety and essential performance; apply the risk management process to ask whether the anomaly can contribute to a hazardous situation (use the ISO 14971 risk file), and link to risk controls.
3. **Investigate and fix:** root cause, fix, regression impact analysis; change goes through change control (see design-change-control).
4. **Verify the fix** and regression-test the affected areas; record results.
5. **Release decision:** compile a list of unresolved anomalies with justification that they do not create unacceptable risk; the approving authority signs off.
6. **Post-release:** field reports re-enter the process; evaluate for field safety corrective action or notification (see complaint-handling).
7. Trend defect data (density, escape rate) to improve the process.

## Practice
- Severity labels (blocker, major, minor) should be mapped to risk language so developers and risk owners use the same terms.
- Regulatory submissions often include the list of known residual anomalies with risk assessment; confirm the expectations for your submission type.

## Verify
- [ ] All anomalies have status and risk evaluation.
- [ ] Release record lists open anomalies and their justification.
- [ ] Field anomalies link to complaint records.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
