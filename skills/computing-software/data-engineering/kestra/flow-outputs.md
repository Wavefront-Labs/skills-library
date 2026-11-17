---
id: computing-software.data-engineering.kestra.flow-outputs
name: flow-outputs
category: computing-software
field: data-engineering
product: kestra
tags: [outputs, outputvalues, subflow, internal-storage, flow-outputs, secrets]
level: practitioner
status: docs-checked
description: "Pass data between Kestra tasks and flows with outputs: OutputValues, referencing task outputs, flow-level outputs, subflow access, and why not to emit secrets."
sources:
  - https://kestra.io/docs/workflow-components/outputs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Reference a task output as `{{ outputs.<task_id>.<attribute> }}`. The `OutputValues` task emits named values.

```yaml
tasks:
  - id: produce_output
    type: io.kestra.plugin.core.output.OutputValues
    values:
      result: my output {{ execution.id }}

  - id: use_output
    type: io.kestra.plugin.core.log.Log
    message: "{{ outputs.produce_output.values.result }}"
```

Large results go to internal storage and return a URI, for example `from: "{{ outputs.output_from_query.uri }}"`.

Flow-level outputs are typed and shown in the Overview tab:

```yaml
outputs:
  - id: final
    type: STRING
    value: "{{ outputs.mytask.values.result }}"
```

A parent reads a child's output through the Subflow task with a double reference: `{{ outputs.subflow.outputs.final }}`.

Warning: do not fetch passwords, secrets or tokens through outputs. Output data is stored in clear text in the backend database, internal storage, logs and API responses. Use Secrets instead.

## Checked

2026-11-04. Confirmed against the Kestra outputs page: outputs.<task_id>.<attribute> syntax, OutputValues, internal storage URIs, typed flow outputs in the Overview tab, the double outputs reference through the Subflow task, clear-text storage warning for secrets. Nothing removed.

Method: documentation only; no commands were run.
