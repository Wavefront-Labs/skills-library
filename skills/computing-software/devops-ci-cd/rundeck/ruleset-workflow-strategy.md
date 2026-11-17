---
id: computing-software.devops-ci-cd.rundeck.ruleset-workflow-strategy
name: ruleset-workflow-strategy
category: computing-software
field: devops-ci-cd
product: rundeck
tags: [rundeck, ruleset-strategy, workflow-strategy, run-after, step-conditions]
level: advanced
status: docs-checked
description: "Write Ruleset workflow strategy rules in Rundeck Enterprise: step selectors, run-at-start and run-after directives, if/unless conditions, AND and OR patterns."
sources:
  - https://raw.githubusercontent.com/rundeck/docs/4.0.x/docs/manual/jobs/workflow-strategies/ruleset.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Choose *Ruleset* on the job's Workflow tab. One rule per line, additive: `STEP [directive] [conditions...]`, with at least a directive or a condition.

Step selectors (brackets required): `[2]` or by case-sensitive label `[Deploy QA]`, `[1,2,3]`, `[1-3]`, `[1-3,5-7]`, `[*]`.

Directives: `run-at-start`, `run-in-sequence`, `run-after:X[,Y]` (after the steps run or are skipped). Names with spaces need quotes: `[Step Two] "run-after:Step One"`.

Conditions: `if:expr`, `unless:expr`. Expressions: `key==str`, `key!=str`, `key=~regex`, `key!~regex`, `!key` (unset), and `>=`, `<=`, `>`, `<` with numbers. No curly braces. Option, Global and Workflow Step variables work; Node context variables do not.

AND: several conditions on one line. OR: repeat the rule on separate lines.

```
[1] run-at-start
[2] run-after:1
[3,4,5] if:option.1>0
[3,4,5] if:option.2==true
```

Fan-out and join:

```
[2] run-after:1
[3] run-after:1
[4] run-after:2,3
```

Gotcha: with many jobs in the graph, the edit page can slow down; set `rundeck.gui.workflowGraph` to `false` (changeable in Configuration Manager without restart).

## Checked

2026-11-04: syntax, selectors, directives, conditions, AND and OR patterns, examples and the graph setting confirmed against the Ruleset Workflow Strategy page.
Method: documentation only; no commands were run.
