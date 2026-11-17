---
id: engineering-technology.aerospace-engineering.matlab-simulink.model-advisor-checks
name: model-advisor-checks
category: engineering-technology
field: aerospace-engineering
product: matlab-simulink
tags: [model-advisor, simulink-check, modeling-standards, model-quality, static-analysis]
level: practitioner
status: docs-checked
description: "Run Simulink Model Advisor checks on aerospace models, configure a check set for your modeling standard, and record results for review."
sources:
  - https://www.mathworks.com/help/slcheck/ref/modeladvisor.run.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Model Advisor checks

**Goal:** catch modelling-standard violations and risky settings before testing or code generation.

## Use
1. Run it from the command line with `ModelAdvisor.run(Systems)` for batch use: the interface runs only one system at a time, the function runs the models or subsystems you list.
2. Pick the check set: `ModelAdvisor.run(Systems, CheckIDList)` runs only the listed check IDs; `ModelAdvisor.run(Systems, 'Configuration', fileName)` runs the checks in a `.json` or `.mat` configuration file. `CheckIDList` and `Configuration` cannot be combined. Which checks are available depends on your installed products.
3. Run, then work through failures and warnings; read what any automatic fix changes.
4. Save the report and archive it with the model revision. `Results = ModelAdvisor.run(...)` returns `ModelAdvisor.SystemResult` objects; for parent models with referenced models the page points to `Advisor.Application`.
5. To enforce a team standard, keep the configuration file under version control; an explicit `Configuration` argument overrides the file attached to the model.

## Practice
- Run on every integration, in continuous integration through a script, not only before release.
- Treat justified deviations as documented waivers, not silently unchecked boxes.
- Re-run after changing solver or data-type settings.

## Gotchas
- Which checks exist, and their names, change between releases; read the list in your release.
- A passing run does not prove the model is correct; it checks style and configuration.
- Do not claim certification credit from the tool alone; compliance is a process decision made with the certification authority.

## Verify
- [ ] The saved report shows zero unreviewed failures for the check set your plan names.

## Checked

2026-11-01. Confirmed on the MathWorks `ModelAdvisor.run` page: purpose, `Systems` / `CheckIDList` / `'Configuration'`
syntax forms, `.json` or `.mat` configuration, `CheckIDList` and `Configuration` cannot be combined, configuration
precedence, `ModelAdvisor.SystemResult` outputs, `Advisor.Application` for referenced models. Removed: Modeling tab
location, Embedded Coder and DO-178C/DO-331 check sets, and Configuration Editor, none of which the page states.
Method: documentation only; no commands were run.
