---
id: engineering-technology.automotive-vehicle-engineering.matlab-simulink.model-advisor-and-modelling-guidelines
name: model-advisor-and-modelling-guidelines
category: engineering-technology
field: automotive-vehicle-engineering
product: matlab-simulink
tags: [model-advisor, modeling-guidelines, misra, iso-26262-checks, naming-rules, simulink-check, model-based-design]
level: practitioner
status: draft
description: "Configure Model Advisor checks to enforce modelling guidelines for production controllers, automate in CI, and manage justified exclusions."
sources:
  - "Simulink Check: ModelAdvisor.run (https://www.mathworks.com/help/slcheck/ref/modeladvisor.run.html)"
  - "MathWorks Advisory Board guidelines, confirm the current edition (https://www.mathworks.com)"
licence: Apache-2.0
version: 5
updated: 2026-11-17
aliases: []
---

# Model Advisor and modelling guidelines

1. Choose a check set matching your standards (the product ships by-task and standards-based sets; availability depends on licence and release).
2. Create a Model Advisor configuration file (.json or .mat) that selects checks and parameters, and keep it under version control.
3. Run `ModelAdvisor.run(system,'Configuration',file)` in CI; fail the build on new failures; archive the HTML report.
4. Exclusions: record each with a reason and reviewer, in the exclusion file, never silently.
5. Typical checks: solver and sample time settings, unsupported blocks, data types, unconnected ports, naming, diagnostics set to error, stateflow semantic checks.
6. Re-run after each model change; keep the result history for the safety case.

**Gotchas:** treating warnings as noise; excluding a check just to pass.

## Verify
- [ ] CI shows zero unapproved failures.
- [ ] Exclusion list reviewed and each entry has a justification.
