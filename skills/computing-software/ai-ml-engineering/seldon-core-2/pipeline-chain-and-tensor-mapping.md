---
id: computing-software.ai-ml-engineering.seldon-core-2.pipeline-chain-and-tensor-mapping
name: pipeline-chain-and-tensor-mapping
category: computing-software
field: ai-ml-engineering
product: seldon-core-2
tags: [seldon-core-2, pipeline, chain, tensormap, step-inputs, output-steps, v2-tensors]
level: practitioner
status: docs-checked
description: "Build a Seldon Core 2 Pipeline that chains models: steps, inputs dot notation, output.steps, and tensorMap renaming so output tensor names match the input names of the next model."
sources: ["https://github.com/SeldonIO/seldon-core/blob/v2/docs-gb/pipelines.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Pipeline chaining and tensorMap

A Pipeline connects Models into a flow of data transformations. The Pipeline resource is accepted on Kubernetes and by the local `seldon` CLI, and both submit it through the Scheduler API.

```yaml
apiVersion: mlops.seldon.io/v1alpha1
kind: Pipeline
metadata:
  name: chain
  namespace: seldon-mesh
spec:
  steps:
    - name: model1
    - name: model2
      inputs:
      - model1
  output:
    steps:
    - model2
```

## Fields
- `steps`: each step name is a Model of the same name. Pipelines can be deployed before or together with their models, but the models must be available for the Pipeline to work.
- `steps.inputs`: sources for the step. The form is `<stepName|pipelineName>.<inputs|outputs>.<tensorName>`. A bare step name means `step.outputs`. Reference one tensor with `mymodel.outputs.t1`.
- `output.steps`: the pipeline output. It is required if you call the Pipeline synchronously over REST/gRPC. Branches such as drift detectors may legitimately not reach the output.

## tensorMap
Payloads use the V2 protocol with named tensors. Chaining works directly only if output tensor names match the input names of the next model; otherwise rename them:

```yaml
    - name: tfsimple2
      inputs:
      - tfsimple1
      tensorMap:
        tfsimple1.outputs.OUTPUT0: INPUT0
        tfsimple1.outputs.OUTPUT1: INPUT1
```

Shape and data type of the tensors must also match.

## Checked

Confirmed against the Seldon Core 2 Pipelines page: steps, steps.inputs dot notation and bare step name meaning step.outputs, output.steps requirement for synchronous calls, V2 named tensors, tensorMap renaming, and the shape and data type match. The tensorMap example is an illustration built from the documented construct.

Method: docs-checked 2026-11-09 against the Seldon Core v2 docs-gb pipelines.md page (raw markdown).
