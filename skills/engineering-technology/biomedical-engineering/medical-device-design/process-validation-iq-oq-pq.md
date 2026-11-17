---
id: engineering-technology.biomedical-engineering.medical-device-design.process-validation-iq-oq-pq
name: process-validation-iq-oq-pq
category: engineering-technology
field: biomedical-engineering
product: medical-device-design
tags: [process-validation, medical-dfm, design-for-manufacture, iq-oq-pq, special-process, ghtf-process-validation, revalidation, process-capability]
level: advanced
status: gated
description: "Validate a device manufacturing process with IQ, OQ and PQ: when it is required, worst-case challenges, sample sizes, acceptance criteria and revalidation triggers."
sources: ["GHTF/SG3/N99-10:2004 (Edition 2) Quality management systems - Process validation guidance, https://www.imdrf.org/sites/default/files/docs/ghtf/final/sg3/technical-docs/ghtf-sg3-n99-10-2004-qms-process-guidance-04010.pdf", "ISO 13485:2016 Medical devices - Quality management systems (production process validation)", "21 CFR Part 820 (QMSR), https://www.ecfr.gov/current/title-21/part-820"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Process validation (IQ, OQ, PQ)

**Goal:** objective evidence that a process consistently produces product meeting specification, when its output cannot be fully verified by later inspection.

Quality-system practice. In the US, 21 CFR Part 820 (the QMSR) incorporates ISO 13485:2016 by reference (eCFR 820.7, 820.10). The IQ/OQ/PQ structure, worst-case limits in OQ and the revalidation triggers below follow GHTF/SG3/N99-10:2004 Edition 2 (January 2004; IMDRF has a revision in progress, so check for a successor). Follow your market's regulation.

## When to validate
Validate where results cannot be fully verified by inspection or test (sealing, sterilisation, welding, moulding of critical features, cleaning, software, coating); otherwise, verify each unit. Decide with a documented risk rationale.

## Stages
1. **Plan:** validation master plan identifies processes, responsibilities, equipment, acceptance criteria and sample plans.
2. **IQ (installation qualification):** equipment installed as specified; utilities, drawings, calibration and software versions recorded.
3. **OQ (operational qualification):** run the process across its operating window including **worst cases** (high/low limits of key parameters) to show conforming output and to define the parameter ranges; use a designed experiment to find critical parameters (DOE) and a challenge of alarms and controls.
4. **PQ (performance qualification):** run under normal conditions with production-equivalent materials, operators and environments, for a defined number of runs or lots (three consecutive conforming runs is a common industry minimum (gated: unconfirmed, source is paywalled or blocked); the GHTF guidance does not set a number, so justify it statistically), with sample sizes tied to confidence and reliability (see confidence-reliability-sampling).
5. **Acceptance:** predefined criteria for each CTQ; process capability (Cpk of at least about 1.33, or higher for critical characteristics, is a common industry convention (gated: unconfirmed, source is paywalled or blocked)) where continuous data permit (see process-capability).
6. **Report and approve.**
7. **Control:** monitor critical parameters, preventive maintenance, calibration, change control.
8. **Revalidation triggers** (GHTF 6.4): change in the process that may affect quality or validation status, negative trend in quality indicators, product design change affecting the process, transfer to another facility, change of application; also evaluate equipment repair, material or supplier change and software change, and review periodically.

## Gotchas
- OQ at nominal only; hidden dependence on edges of the window.
- Using engineering lots with different operators from production.
- Software that controls the process is itself validated.
- Not validating the measurement methods used in the validation (see tmv-procedure).

## Verify
- [ ] Protocol approved before execution; deviations documented.
- [ ] Worst-case conditions represented in OQ.
- [ ] PQ results meet capability and acceptance criteria.
