---
id: computing-software.devops-ci-cd.rundeck.pass-data-between-steps
name: pass-data-between-steps
category: computing-software
field: devops-ci-cd
product: rundeck
tags: [rundeck, step-data-variables, context-variables, node-vs-workflow-steps, log-data-step]
level: practitioner
status: docs-checked
description: "Share data between Rundeck job steps with log filters: variable syntax for command and script steps, and reading node step values from workflow steps."
sources:
  - https://raw.githubusercontent.com/rundeck/docs/4.0.x/docs/learning/howto/passing-variables.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Context variable sets: `job`, `node`, `option` and step data `data`. Step data comes from log filters applied to a step's output and is held in memory while the job runs.

Syntax:
- Options: `${option.input_key}` in command steps, `@option.input_key@` in scripts.
- Step data: `${data.MyKeyName}` in command steps, `@data.MyKeyName@` in scripts.

Example job from the page: step 1 runs `hostname` with a log filter naming the variable `MyKeyName`; step 2 (command) uses `${data.MyKeyName}`; step 3 (script) uses `@data.MyKeyName@`.

Node steps run once per matching node and store data in node scope; workflow steps run once on the Rundeck server and store data in global scope. With several nodes, each node step creates a variable per node.

Common sticking point: a workflow step reading a node step's value must name the node:

```
${data.MyKeyName@hostname}
```

`${data.MyKeyName*}` joins values from all nodes with a comma; add a separator after the star to change it, as in `${data.MyKeyName*;}`.

Debug by adding the Log Data Step (workflow step) to print what is available.

## Checked

2026-11-04: context sets, syntax for command steps and scripts, node versus workflow step scope, the @node form and the * join confirmed against the Pass Data Between Steps how-to.
Method: documentation only; no commands were run.
