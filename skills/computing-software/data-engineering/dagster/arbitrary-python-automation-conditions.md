---
id: computing-software.data-engineering.dagster.arbitrary-python-automation-conditions
name: arbitrary-python-automation-conditions
category: computing-software
field: data-engineering
product: dagster
tags: [dagster, custom-automation-condition, use-user-code-server, entitysubset, evaluate, candidate-subset]
level: advanced
status: docs-checked
description: "Write a custom Dagster AutomationCondition subclass with evaluate(), and run the sensor on the user code server via use_user_code_server (preview)."
sources:
  - https://docs.dagster.io/guides/automate/declarative-automation/customizing-automation-conditions/arbitrary-python-automation-conditions
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Arbitrary Python automation conditions (preview)

Goal: express business logic (for example skip company holidays) beyond the built-ins.

## Setup
Automation condition sensors normally run in a daemon without your user code. Add an automation condition sensor to your definitions with `use_user_code_server=True`, so it evaluates where `@sensor` functions run. Evaluation can be resource-intensive: a limit of 500 assets or checks per sensor is enforced.

## Define
Subclass `AutomationCondition` and implement `evaluate()`. Return a subset using `EntitySubsets` rather than a plain boolean, since partitions of a partitioned asset can differ. For the holiday example: not a holiday returns the empty subset; holiday returns `candidate_subset`. The candidate subset shrinks through `&`: if `A` returns empty, the candidate subset for `B` in `A & B` is empty, avoiding expensive work. Then use it in a broader expression with the built-ins.

## Checked

2026-11-03. Pages read in full against this skill:
- https://docs.dagster.io/guides/automate/declarative-automation/customizing-automation-conditions/arbitrary-python-automation-conditions

Confirmed: the identifiers, settings, defaults, numbers and behaviours stated above, against the page text and its code examples.
Removed or reworded: nothing; every concrete claim matched the page.

Method: documentation only; no commands were run.
