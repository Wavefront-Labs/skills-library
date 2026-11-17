---
id: computing-software.devops-ci-cd.rundeck.conditional-logic-steps
name: conditional-logic-steps
category: computing-software
field: devops-ci-cd
product: rundeck
tags: [rundeck, conditional-logic, node-conditional, workflow-conditional, feature-flag]
level: advanced
status: docs-checked
description: "Branch Rundeck job workflows with Conditional Logic steps (commercial): node vs workflow type, available fields, limitations and the feature flag."
sources:
  - https://raw.githubusercontent.com/rundeck/docs/4.0.x/docs/manual/jobs/conditional-logic.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Commercial feature. Generally available and on by default from Runbook Automation 6.3.0. In 5.20.0 to 6.2.x it is early access:

```properties
rundeck.feature.earlyAccessJobConditional.enabled=true
```

Restart after changing it (self-hosted). Set `false` to disable on 6.3.0+.

Gotcha: with the flag off, jobs containing conditional steps fail to run. Opening such a job in the editor strips the steps and shows "Conditional logic steps removed"; saving then removes them permanently.

Add via Add a step, then Node Steps or Workflow Steps tab. Name each step uniquely so later conditions can reference its outputs on the Prior Steps tab.

- Node Conditional Logic: evaluated per node. Fields: job context, prior node step outputs, node attributes, options, log-filter data. Example: `${node.osFamily}` equals `unix`.
- Workflow Conditional Logic: evaluated once on the server. No node attributes or node step outputs. Example: `${option.environment}` equals `production`, or `${data.status}` equals `ready`.

Operators include equals, not equals, contains, regex match, numeric comparisons. Conditions in a set are ANDed by default; an AND/OR toggle changes grouping. Debug mode logs condition evaluation.

Limits:
- not supported with the Ruleset strategy (Sequential, Parallel, Node First work)
- substeps and referenced prior steps must match the parent's type
- nesting is one level: a nested conditional cannot hold another

Verify by running with debug mode and reading the evaluation lines in the log.

## Checked

2026-11-04. Confirmed against the Rundeck docs page Conditional Logic Steps (Commercial): GA and default-on in 6.3.0, early access flag rundeck.feature.earlyAccessJobConditional.enabled for 5.20.0 to 6.2.x, restart for self-hosted, behaviour when the flag is turned off, node vs workflow type and their fields, operators, AND/OR toggle, debug mode, and the three limitations. Nothing removed.

Method: documentation only; no commands were run.
