---
id: computing-software.cloud-infrastructure-engineering.crossplane.composition-pipeline-mode
name: composition-pipeline-mode
category: computing-software
field: cloud-infrastructure-engineering
product: crossplane
tags: [composition, pipeline, function, mode]
level: practitioner
status: docs-checked
description: "Build a Crossplane Composition as a mode Pipeline of function steps, with functionRef and optional input per step."
sources:
  - https://docs.crossplane.io/latest/composition/compositions/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A Composition is a pipeline of composition functions. Set `spec.mode: Pipeline`, then list `spec.pipeline` steps. Each step has a `step` name, a `functionRef.name`, and optionally an `input` whose kind the function defines.

```yaml
spec:
  compositeTypeRef:
    apiVersion: custom-api.example.org/v1alpha1
    kind: AcmeBucket
  mode: Pipeline
  pipeline:
  - step: patch-and-transform
    functionRef:
      name: function-patch-and-transform
    input:
      apiVersion: pt.fn.crossplane.io/v1beta1
      kind: Resources
```

Crossplane calls steps in order and passes each function the result of the previous one. That lets you combine, for example, function-cue to create a bucket and then function-auto-ready to mark the XR ready when the bucket is.

Rules to remember:

- `compositeTypeRef` (apiVersion and kind) limits which composite resource type can use the Composition. It must match the XRD.
- Crossplane does not validate function input. Have the function validate its own input.
- Functions do not run when an XR is deleted. Crossplane deletes composed resources itself.
- List Compositions with `kubectl get composition`; the XR-KIND and XR-APIVERSION columns show which XRs may use each one.

## Checked

2026-11-03. Confirmed against the Crossplane docs (Compositions page, docs.crossplane.io/latest): the field names, values, defaults and behaviours stated above. Removed or reworded: nothing.

Method: documentation only; no commands were run.
