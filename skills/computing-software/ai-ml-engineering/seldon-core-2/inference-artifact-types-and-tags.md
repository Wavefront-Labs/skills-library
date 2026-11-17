---
id: computing-software.ai-ml-engineering.seldon-core-2.inference-artifact-types-and-tags
name: inference-artifact-types-and-tags
category: computing-software
field: ai-ml-engineering
product: seldon-core-2
tags: [seldon-core-2, inference-artifacts, requirements, mlserver, triton, sklearn, xgboost, tensorflow, pytorch, onnx, model-settings]
level: practitioner
status: docs-checked
description: "Which artifact types run on MLServer or Triton, the requirements tag each needs, how to save each, and where model-settings.json or config.pbtxt goes."
sources: ["https://github.com/SeldonIO/seldon-core/blob/v2/docs-gb/models/inference-artifacts.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Inference artifact types and requirement tags

The tag in the table below is what you put in the Model `spec.requirements` so the artifact lands on a compatible server.

| Type | Server | Tag | Save as |
|---|---|---|---|
| SKLearn | MLServer | `sklearn` | joblib `.joblib`, or pickle `.pkl` / `.pickle` |
| XGBoost | MLServer | `xgboost` | `.bst` or `.json` |
| LightGBM | MLServer | `lightgbm` | `.bst` |
| MLFlow | MLServer | `mlflow` | the `artifacts/model` folder of the run |
| Huggingface | MLServer | `huggingface` | MLServer `model-settings.json` naming the model |
| Alibi-Detect | MLServer | `alibi-detect` | saved with Alibi-Detect |
| Alibi-Explain | MLServer | `alibi-explain` | saved with Alibi-Explain |
| Custom Python | MLServer | `python, mlserver` | class extending `MLModel` |
| Custom Python | Triton | `python, triton` | `config.pbtxt` plus python files |
| ONNX | Triton | `onnx` | `model.onnx` |
| PyTorch | Triton | `pytorch` | traced torchscript as `model.pt` with `config.pbtxt` |
| Tensorflow | Triton | `tensorflow` | SavedModel format; HDF5 not supported |
| Spark Mlib | MLServer | `spark-mlib` | follow the MLServer docs |
| TensorRT, DALI, OpenVino, FIL | Triton | `tensorrt`, `dali`, `openvino`, `fil` | follow the Triton backend docs |

## Custom settings
- MLServer models: place a `model-settings.json` alongside the artifact.
- Triton models: place a `config.pbtxt` alongside the artifact.

```yaml
spec:
  storageUri: "gs://seldon-models/scv2/samples/mlserver_1.5.0/iris-sklearn"
  requirements:
  - sklearn
  memory: 100Ki
```

## Checked
Method: docs-checked 2026-11-09 against docs-gb/models/inference-artifacts.md (read in full). Added the Spark Mlib row from the page.
