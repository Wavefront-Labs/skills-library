---
id: computing-software.cloud-infrastructure-engineering.graylog.pipelines-stages-and-rules
name: pipelines-stages-and-rules
category: computing-software
field: cloud-infrastructure-engineering
product: graylog
tags: [pipelines, pipeline-rules, stages, rule-builder, functions]
level: practitioner
status: docs-checked
description: "Graylog processing pipelines: rules, stages run in numeric order, functions and the rule builder; watch Processing Errors."
sources:
  - https://go2docs.graylog.org/current/making_sense_of_your_log_data/pipelines.html
  - https://go2docs.graylog.org/current/making_sense_of_your_log_data/rules.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# pipelines stages and rules

Pipelines are collections of rules applied in **stages**, attached to streams. Messages sent to a stream first pass through attached pipelines.

- **Rules**: a condition plus an action. Actions route messages to streams, extract or rename fields, transform or enrich.
- **Functions**: built-in building blocks with parameters and return values (conversion, string handling, lookups).
- **Stages**: run sequentially in numerical order; all stages with the same number run together.
- **Rule builder**: the main interface, with testing before deployment. The source code editor is the manual alternative.

Rules are sensitive to data types, so check types in conditions and actions.

Monitor the **Processing Errors** column on the Pipelines page, which sums errors from all rules in the pipeline for all time. A typical error is a rule putting a datetime value into a number field.

Rule source: a rule is `rule "name" when <boolean condition> then <actions> end`. A stage declares `match all` (every rule condition must be true to continue to later stages) or `match either` (one is enough); actions still run for every matching rule. Stage numbers can be any integer, positive or negative. Do not use reserved words such as `match`, `stage` or `let` as variable names. Compare like types only: comparing different data types evaluates to false, so convert with the `to_` functions first.

## Checked

Method: docs-checked 2026-11-09 against https://go2docs.graylog.org/current/making_sense_of_your_log_data/pipelines.html and https://go2docs.graylog.org/current/making_sense_of_your_log_data/rules.html (both read in full, Graylog 7.2 docs).
