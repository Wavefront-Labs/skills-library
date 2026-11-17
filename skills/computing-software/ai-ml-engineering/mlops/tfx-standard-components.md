---
id: computing-software.ai-ml-engineering.mlops.tfx-standard-components
name: tfx-standard-components
category: computing-software
field: ai-ml-engineering
product: mlops
tags: [mlops, tfx-components, tfx, tensorflow-transform, tfma, ml-pipelines]
level: practitioner
status: docs-checked
description: "Build a TFX pipeline from standard components: ExampleGen to Pusher, Transform preprocessing_fn, Evaluator blessing against a baseline, InfraValidator."
sources:
  - https://www.tensorflow.org/tfx/guide
  - https://www.tensorflow.org/tfx/guide/evaluator
  - https://www.tensorflow.org/tfx/guide/transform
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# TFX standard components

**Goal:** a production TensorFlow pipeline where data is validated, preprocessing is consistent between training and serving, and only models that pass validation are pushed.

## Components named in the TFX guide
`ExampleGen` (ingest), `StatisticsGen`, `SchemaGen`, `ExampleValidator`, `Transform`, `Trainer` (with an optional `Tuner` before it), `Evaluator`, `InfraValidator` and `Pusher`. Libraries underneath include TensorFlow Data Validation, TensorFlow Transform, TensorFlow Model Analysis and ML Metadata (MLMD).

## Transform
Specify preprocessing with a `preprocessing_fn` written in TensorFlow code plus TensorFlow Transform analyzers, supplied to the Transform component as a module. The result is a SavedModel that the Trainer imports, so the exported model includes the data engineering transformations; the guide describes this as guaranteeing consistency between training and serving.
```python
import tensorflow_transform as tft
def preprocessing_fn(inputs):
    return {"amount_z": tft.scale_to_z_score(inputs["amount"])}
```

## Evaluator and validation
The Evaluator computes metrics over slices of data and, when validation is enabled, compares a new model against a baseline (such as the currently serving model) using metric thresholds (for example AUC not lower than the baseline). If the criteria are met the model is "blessed". The baseline choice (for example latest blessed model) is configured in the pipeline.

## InfraValidator and Pusher
`InfraValidator` launches a canary TensorFlow Serving model server to actually serve the SavedModel; if validation passes, `Pusher` deploys the SavedModel to the serving target.

## Trainer note
For use with TFMA, the guide says the training code should save the model as both a SavedModel and an EvalSavedModel.

## Checked
Method: docs-checked 2026-11-09 against the TFX guide, Evaluator guide and Transform guide (downloaded HTML, searched and read the component, validation and preprocessing_fn sections). Dropped the component table details, the Resolver and EvalConfig example, the Vertex AI Pipelines runner section, caching, gotchas about version pinning, Dataflow advice and the Vertex tutorial source (not read).
