---
id: computing-software.data-engineering.kestra.flow-labels
name: flow-labels
category: computing-software
field: data-engineering
product: kestra
tags: [labels, metadata, filtering, labels-task, trigger-labels]
level: intro
status: docs-checked
description: "Attach key-value labels to Kestra flows and executions, set them in YAML, at launch, after the run, from the Labels task, or from trigger expressions."
sources:
  - https://kestra.io/docs/workflow-components/labels
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Labels are key-value pairs on flows and executions. Unlike the namespace hierarchy, they let you group and filter across any dimension (team, project, environment, priority).

```yaml
id: process_invoice_flow
namespace: company.team

labels:
  team: finance
  priority: HIGH

tasks:
  - id: hello
    type: io.kestra.plugin.core.log.Log
    message: hello from a flow with labels
```

Executions inherit the flow's labels. Other ways to set them:

- At launch: Advanced configuration in the Execute modal (set or override).
- After execution: Set labels on the Overview tab, or in bulk from the bulk action menu.
- During execution: the `io.kestra.plugin.core.execution.Labels` task, with a map (static key, dynamic value) or a list of key-value objects (dynamic key and value). It can override flow-level defaults.
- In triggers: a `labels` block accepting Pebble, such as `"year-{{now(format='YYYY')}}"` or `"{{trigger.previous}}"`.

Static values and expressions can be mixed in one trigger `labels` block. Available trigger variables depend on the trigger type.

## Checked

2026-11-04. Confirmed against the Kestra labels page: key-value labels on flows and executions, inheritance, Execute modal Advanced configuration, Set labels on the Overview tab and bulk setting, the Labels task with map or list forms and override, Pebble labels in triggers, mixing static and dynamic values. Nothing removed.

Method: documentation only; no commands were run.
