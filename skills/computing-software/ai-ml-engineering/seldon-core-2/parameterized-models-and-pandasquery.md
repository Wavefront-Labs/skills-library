---
id: computing-software.ai-ml-engineering.seldon-core-2.parameterized-models-and-pandasquery
name: parameterized-models-and-pandasquery
category: computing-software
field: ai-ml-engineering
product: seldon-core-2
tags: [seldon-core-2, parameterized-models, pandasquery, conditional-routing, triggers, mlserver, model-settings]
level: advanced
status: docs-checked
description: "Pass parameters into a custom MLServer model, such as the PandasQuery row filter, and use two parameterized models as triggers for conditional pipeline routing."
sources: ["https://github.com/SeldonIO/seldon-core/blob/v2/docs-gb/models/parameterized-models/pandasquery.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Parameterized models and PandasQuery

The Model spec can pass named parameters to the model through its `parameters` list; the PandasQuery example below uses a `query` parameter.

```yaml
apiVersion: mlops.seldon.io/v1alpha1
kind: Model
metadata:
  name: choice-is-one
spec:
  storageUri: "gs://seldon-models/scv2/examples/pandasquery"
  requirements:
  - mlserver
  - python
  parameters:
  - name: query
    value: "choice == 1"
```

## PandasQuery
This example model runs a Pandas query on the input to select rows. It also returns a `status` tensor with the operation and whether it succeeded. If no rows match, only `status` is returned.

## Conditional routing
Two instances with queries `choice == 1` and `choice == 2` can drive trigger inputs in a Pipeline:

```yaml
spec:
  steps:
  - name: choice-is-one
  - name: mul10
    inputs:
    - choice.inputs.INPUT
    triggers:
    - choice-is-one.outputs.choice
  - name: choice-is-two
  - name: add10
    inputs:
    - choice.inputs.INPUT
    triggers:
    - choice-is-two.outputs.choice
  output:
    steps:
    - mul10
    - add10
    stepsJoin: any
```

`mul10` runs if `choice-is-one` succeeds; `add10` runs if `choice-is-two` succeeds.

## Checked
Method: docs-checked 2026-11-09 against docs-gb/models/parameterized-models/pandasquery.md (read in full). Dropped an unsupported claim about model-settings.json parameters.extra and the MLServer load method.
