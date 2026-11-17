---
id: computing-software.ai-ml-engineering.seldon-core-2.pipeline-conditional-routing
name: pipeline-conditional-routing
category: computing-software
field: ai-ml-engineering
product: seldon-core-2
tags: [seldon-core-2, pipeline, conditional-routing, multi-armed-bandit, error-abort, any-join, tensors]
level: practitioner
status: docs-checked
description: "Route data conditionally in Seldon Core 2 pipelines by having a model emit different named tensors, aborting on errors, and joining branches with stepsJoin any."
sources: ["https://github.com/SeldonIO/seldon-core/blob/v2/docs-gb/pipelines.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Conditional routing in pipelines

## Routing via tensors
The simplest method is a model that outputs different named tensors depending on its decision. Downstream steps depend on different tensors, so only one path runs per request.

```yaml
apiVersion: mlops.seldon.io/v1alpha1
kind: Pipeline
metadata:
  name: tfsimple-conditional
spec:
  steps:
  - name: conditional
  - name: mul10
    inputs:
    - conditional.outputs.OUTPUT0
    tensorMap:
      conditional.outputs.OUTPUT0: INPUT
  - name: add10
    inputs:
    - conditional.outputs.OUTPUT1
    tensorMap:
      conditional.outputs.OUTPUT1: INPUT
  output:
    steps:
    - mul10
    - add10
    stepsJoin: any
```

The `conditional` model emits either `OUTPUT0` or `OUTPUT1`. The final `any` join returns whichever data arrives from either branch. This shape suits multi-armed bandit routing.

## Aborting on error
A pipeline can be aborted when a step produces an error, which acts as a condition. A step such as `outlier-error` runs normally or raises an error depending on the values in the input tensors:

```yaml
spec:
  steps:
    - name: outlier-error
  output:
    steps:
    - outlier-error
```

For gating without passing data, use triggers. For parameterised filter models see the PandasQuery skill.

## Checked

Confirmed against the Seldon Core 2 Pipelines page: routing via different named output tensors, the tfsimple-conditional manifest with stepsJoin any, the multi-armed bandit remark, and aborting a pipeline on error with the outlier-error example.

Method: docs-checked 2026-11-09 against the Seldon Core v2 docs-gb pipelines.md page (raw markdown).
