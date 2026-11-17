---
id: engineering-technology.biomedical-engineering.device-verification-validation.software-unit-testing
name: software-unit-testing
category: engineering-technology
field: biomedical-engineering
product: device-verification-validation
tags: [software-unit-testing, software-verification, iec-62304-testing, unit-test, integration-test, code-coverage, static-analysis, regression-testing]
level: practitioner
status: draft
description: "Plan and execute unit and integration testing for IEC 62304: acceptance criteria, coverage by class, static analysis, test tool validation, regression and traceability."
sources: ["IEC 62304 Medical device software - Software life cycle processes (clauses 5.5 to 5.7; confirm edition)", "FDA, Content of Premarket Submissions for Device Software Functions (current guidance text at https://www.fda.gov)", "MISRA C guidelines (https://misra.org.uk) and ISO/IEC/IEEE 29119 Software testing"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Unit and integration testing under IEC 62304

**Goal:** verified software units and integration, with evidence proportional to the safety class.

## Structure
- **Unit implementation and verification** (5.5): code each software unit; define acceptance criteria; verify (for Class B and C, units are verified against criteria; Class C also requires additional criteria such as boundary conditions and detailed design verification).
- **Integration and integration testing** (5.6): combine units and test interfaces and behaviour.
- **System testing** (5.7): test against software requirements (including risk control measures).
- Release only after verification evidence (5.8).

## Practical plan
1. **Acceptance criteria per unit:** from detailed design or requirements: correct outputs, error handling, memory and timing limits, coding standard compliance.
2. **Test design techniques:** requirement-based tests, equivalence classes and boundary values, error guessing, state-transition tests, fault injection for risk controls (see software-risk-control).
3. **Coverage:** measure statement and branch coverage; set targets by class (for example 100% statement and a high branch target for Class C; justify uncovered code). Coverage is a measurement, not a proof of correctness.
4. **Static analysis and review:** run a static analyser with a coding standard (MISRA C or CERT) and review high-risk units; resolve or justify warnings.
5. **Automation:** continuous integration runs unit tests, static analysis and builds from controlled configuration.
6. **Tool control:** test frameworks, compilers and analysers that affect verification are qualified or validated for intended use (ISO 13485 and FDA expectations for software used in the quality system).
7. **Traceability:** requirement to design to unit to test case to result, kept in a tool or matrix (see traceability-matrix).
8. **Regression:** re-run the relevant tests after every change, with the scope justified by the change impact analysis.
9. **Anomalies:** log defects with severity and disposition; known anomalies at release are evaluated for safety (see software-anomaly-management).

## Gotchas
- Tests that do not check outputs.
- Mocked interfaces hiding timing or protocol issues; add hardware-in-the-loop tests.
- Unrecorded test environments and builds.

## Verify
- [ ] Test records identify software version, environment and tester or tool version.
- [ ] Coverage and static analysis results attached to the release record.
- [ ] Traceability complete for all software requirements and risk controls.
