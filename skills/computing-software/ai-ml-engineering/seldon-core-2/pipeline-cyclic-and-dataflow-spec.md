---
id: computing-software.ai-ml-engineering.seldon-core-2.pipeline-cyclic-and-dataflow-spec
name: pipeline-cyclic-and-dataflow-spec
category: computing-software
field: ai-ml-engineering
product: seldon-core-2
tags: [seldon-core-2, pipeline, cyclic-pipelines, allowcycles, maxsteprevisits, cleantopicsondelete, dataflow, batch]
level: advanced
status: docs-checked
description: "Pipeline spec details: allowCycles with maxStepRevisits for feedback loops, dataflow.cleanTopicsOnDelete, and per-step batch size, windowMs and rolling."
sources: ["https://github.com/SeldonIO/seldon-core/blob/v2/docs-gb/kubernetes/resources/pipeline.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Cyclic pipelines and other Pipeline spec fields

## Cyclic pipelines
Core 2 supports feedback loops in the inference graph, with care. The risk is joining messages from different iterations: a message from iteration t might be joined with messages from t-1, t-2 and so on if a feedback message re-enters within the join window and reaches a step already holding earlier messages.

Enable cycles and bound revisits:

```yaml
apiVersion: mlops.seldon.io/v1alpha1
kind: Pipeline
metadata:
  name: pipeline
spec:
  allowCycles: true
  maxStepRevisits: 100
```

`maxStepRevisits` limits how often a step can be revisited in a single execution. When the limit is reached the execution terminates with an error.

## Other spec fields
- `dataflow.cleanTopicsOnDelete` (default false): delete the Kafka input and output topics when the pipeline is deleted.
- Per step `batch`: `size`, `windowMs` and `rolling`, requiring a batch of requests before data is sent to the step.
- Per step `joinWindowMs`, `inputsJoinType`, `triggersJoinType`, `tensorMap`, `triggers`.
- `input` with `externalInputs` and `externalTriggers`.
- `output` with `steps`, `joinWindowMs`, `stepsJoin`, `tensorMap`.

Join types are `inner` (default), `outer` and `any`.

## Checked

Confirmed against the Pipeline resource page: cyclic pipeline risk text, allowCycles and maxStepRevisits behaviour, dataflow.cleanTopicsOnDelete default false, the batch fields size, windowMs and rolling, the step, input and output field lists, and the inner default with outer and any join types.

Method: docs-checked 2026-11-09 against the Seldon Core v2 docs-gb kubernetes/resources/pipeline.md page (raw markdown).
