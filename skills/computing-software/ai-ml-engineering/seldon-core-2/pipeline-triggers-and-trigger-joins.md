---
id: computing-software.ai-ml-engineering.seldon-core-2.pipeline-triggers-and-trigger-joins
name: pipeline-triggers-and-trigger-joins
category: computing-software
field: ai-ml-engineering
product: seldon-core-2
tags: [seldon-core-2, pipeline, triggers, triggersjointype, externaltriggers, gating]
level: advanced
status: docs-checked
description: "Gate a Seldon Core 2 pipeline step on the output of another step with triggers, and combine multiple triggers using triggersJoinType inner or any without passing trigger data on."
sources: ["https://github.com/SeldonIO/seldon-core/blob/v2/docs-gb/pipelines.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Pipeline triggers and trigger joins

A trigger makes a step run when an output is received from another step, without sending that data into the model.

```yaml
spec:
  steps:
    - name: tfsimple1
    - name: tfsimple2
    - name: check
      inputs:
      - tfsimple1.outputs.OUTPUT0
      tensorMap:
        tfsimple1.outputs.OUTPUT0: INPUT
    - name: tfsimple3
      inputs:
      - tfsimple1.outputs.OUTPUT0
      - tfsimple2.outputs.OUTPUT1
      tensorMap:
        tfsimple1.outputs.OUTPUT0: INPUT0
        tfsimple2.outputs.OUTPUT1: INPUT1
      triggers:
      - check.outputs.OUTPUT
  output:
    steps:
    - tfsimple3
```

`tfsimple3` runs only when `tfsimple1`, `tfsimple2` and `check` all produced data, but it receives only the join of the first two.

## Multiple triggers
List several triggers and choose how they combine with `triggersJoinType`:

```yaml
spec:
  steps:
  - name: mul10
    inputs:
    - trigger-joins.inputs.INPUT
    triggers:
    - trigger-joins.inputs.ok1
    - trigger-joins.inputs.ok2
    triggersJoinType: any
```

With `any`, data on `ok1` or `ok2` runs `mul10`. Changing to `inner` requires both. Triggers can be optional pipeline input tensors, as here.

Pipelines can also take triggers from other pipelines through `input.externalTriggers`.

## Checked

Confirmed against the Pipelines page: the joincheck trigger example, the behaviour that the triggered step receives only the join of its inputs, the trigger-joins example with triggersJoinType any versus inner, and externalTriggers.

Method: docs-checked 2026-11-09 against the Seldon Core v2 docs-gb pipelines.md page (raw markdown).
