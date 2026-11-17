---
id: computing-software.ai-ml-engineering.seldon-core-2.pipeline-to-pipeline-inputs
name: pipeline-to-pipeline-inputs
category: computing-software
field: ai-ml-engineering
product: seldon-core-2
tags: [seldon-core-2, pipeline, externalinputs, pipeline-to-pipeline, shared-dataflows, input]
level: advanced
status: docs-checked
description: "Make one Seldon Core 2 pipeline consume the inputs, outputs or step data of another pipeline with spec.input.externalInputs, tensorMap and externalTriggers, and know the caveats."
sources: ["https://github.com/SeldonIO/seldon-core/blob/v2/docs-gb/pipelines.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Pipeline-to-pipeline inputs

By default a Pipeline is called synchronously over HTTP/gRPC or asynchronously via its Kafka topic. You can also build a Pipeline that takes its input from other pipelines using an `input` section. This extends a running pipeline and shares its data flows.

Given an existing pipeline `tfsimple` whose output is the step `tfsimple1`, a second one can consume it:

```yaml
apiVersion: mlops.seldon.io/v1alpha1
kind: Pipeline
metadata:
  name: tfsimple-extended
spec:
  input:
    externalInputs:
      - tfsimple.outputs
    tensorMap:
      tfsimple.outputs.OUTPUT0: INPUT0
      tfsimple.outputs.OUTPUT1: INPUT1
  steps:
    - name: tfsimple2
  output:
    steps:
    - tfsimple2
```

## Reference forms in externalInputs
- `<pipelineName>.(inputs|outputs).<tensorName>`
- `<pipelineName>.(step).<stepName>.<tensorName>`

Tensor names are optional and needed only to take a single tensor. The `input` section also has `externalTriggers`, `joinWindowMs`, `joinType` and `triggersJoinType`, following the same spec as a step.

## Caveats
- Circular dependencies between pipelines are not detected.
- Pipeline status is local to each pipeline.

## Checked

Confirmed against the Pipelines page and the Pipeline resource page: the tfsimple-extended example, the two externalInputs reference forms, optional tensor names, externalTriggers, the two present caveats, and the input fields externalTriggers, joinWindowMs, joinType and triggersJoinType.

Method: docs-checked 2026-11-09 against the Seldon Core v2 docs-gb pipelines.md and kubernetes/resources/pipeline.md pages (raw markdown).
