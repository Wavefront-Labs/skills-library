---
id: computing-software.ai-ml-engineering.seldon-core-2.pipeline-joins-and-join-types
name: pipeline-joins-and-join-types
category: computing-software
field: ai-ml-engineering
product: seldon-core-2
tags: [seldon-core-2, pipeline, join, inputsjointype, joinwindowms, inner, outer, any, stepsjoin]
level: practitioner
status: docs-checked
description: "Join outputs of several steps into one Seldon Core 2 pipeline step, and choose inner, outer or any join semantics with inputsJoinType and joinWindowMs."
sources: ["https://github.com/SeldonIO/seldon-core/blob/v2/docs-gb/pipelines.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Pipeline joins

Joining combines outputs from multiple steps as input to a new step.

```yaml
apiVersion: mlops.seldon.io/v1alpha1
kind: Pipeline
metadata:
  name: join
spec:
  steps:
    - name: tfsimple1
    - name: tfsimple2
    - name: tfsimple3
      inputs:
      - tfsimple1.outputs.OUTPUT0
      - tfsimple2.outputs.OUTPUT1
      tensorMap:
        tfsimple1.outputs.OUTPUT0: INPUT0
        tfsimple2.outputs.OUTPUT1: INPUT1
  output:
    steps:
    - tfsimple3
```

Here the pipeline inputs go to two models, then one output tensor from each feeds the last model. Unused outputs are simply not captured.

## Join types
Set `inputsJoinType` on a step (default `inner`):
- `inner`: all inputs must be available to join.
- `outer`: wait `joinWindowMs` and join whatever has arrived, ignoring inputs that sent nothing. The step therefore has latency of at least `joinWindowMs`.
- `any`: wait for any of the specified sources.

The same idea applies on the output side with `output.stepsJoin` (and `output.joinWindowMs`), for example `stepsJoin: any` to return whichever branch produced data. Other join fields are `triggersJoinType` for triggers and `input.joinType` for pipeline inputs.

`joinWindowMs` is the number of milliseconds to wait for messages from multiple inputs to arrive before joining them.

## Checked

Confirmed against the Pipelines page and the Pipeline resource page: the join example, inner, outer and any semantics, the inner default for inputsJoinType, and the joinWindowMs, stepsJoin, triggersJoinType and input.joinType fields. Removed the claim that joins are a Kafka Streams concept that bounds record holding, replacing it with the spec wording for joinWindowMs.

Method: docs-checked 2026-11-09 against the Seldon Core v2 docs-gb pipelines.md and kubernetes/resources/pipeline.md pages (raw markdown).
