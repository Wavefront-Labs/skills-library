---
id: engineering-technology.aerospace-engineering.matlab-simulink.requirements-based-testing-and-coverage
name: requirements-based-testing-and-coverage
category: engineering-technology
field: aerospace-engineering
product: matlab-simulink
tags: [matlab, simulink, model-based-verification, requirements-based-testing, requirements-toolbox, model-coverage, mcdc, do-178c, do-331]
level: advanced
status: verified
description: "Link requirements to Simulink tests and measure model coverage, including the structural coverage levels linked to DO-178C design assurance levels."
sources:
  - "MathWorks Requirements Toolbox and Simulink Coverage documentation"
  - "RTCA DO-178C and DO-331 (software and model-based development supplement)"
  - "EUROCAE ED-12C"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Requirements-based testing and coverage

**Goal:** evidence that tests trace to requirements and exercise the model structure.

## Steps
1. Author or import requirements (Requirements Toolbox); link them to model elements and tests (traceability matrix).
2. Write tests for each requirement (normal and robustness cases).
3. Run with Simulink Coverage enabled: decision, condition, and modified condition/decision coverage (MC/DC) metrics on model elements.
4. Review uncovered elements: add tests for missing requirements-based behaviour, or document dead code, derived requirements and deactivated code.

## Context (airborne software)
DO-178C (ED-12C) sets objectives by software level: structural coverage objectives accumulate by level: statement coverage at level C, plus decision coverage at level B, plus MC/DC at level A (gated: unconfirmed, source is paywalled or blocked). DO-331 is the supplement for model-based development. Coverage must come from requirements-based tests, not just from coverage-driven added tests. Whether a tool or workflow satisfies the objectives is for the applicant and certification authority to agree; tools may need qualification (DO-330).

## Gotchas
- 100% coverage with poor requirements is not verification.
- Model coverage and code coverage are different artefacts: under DO-331 evidence needs agreement with the authority.

## Verify
- [ ] Traceability matrix shows every requirement has at least one test and every test traces to a requirement.
