---
id: computing-software.ai-ml-engineering.kserve.kserve-servingruntime-clusterservingruntime
name: kserve-servingruntime-clusterservingruntime
category: computing-software
field: ai-ml-engineering
product: kserve
tags: [servingruntime, clusterservingruntime, supportedmodelformats, runtimeversion, storagehelper, model-formats, custom-runtime, template-variables, kserve-mlserver, kserve-tritonserver]
level: practitioner
status: docs-checked
description: "Define reusable serving runtimes with ServingRuntime and ClusterServingRuntime: spec attributes, built-in runtimes, template variables, runtimeVersion, legacy schema."
sources: ["https://github.com/kserve/website/blob/main/docs/concepts/resources/servingruntime.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# ServingRuntime and ClusterServingRuntime

Both CRDs (`serving.kserve.io/v1alpha1`) are pod templates for one or more model formats; the only difference is scope (namespace vs cluster). Add custom runtimes without touching controller code.

```yaml
apiVersion: serving.kserve.io/v1alpha1
kind: ServingRuntime
metadata:
  name: example-runtime
spec:
  supportedModelFormats:
    - name: example-format
      version: "1"
      autoSelect: true
  containers:
    - name: kserve-container
      image: examplemodelserver:latest
      args: [--model_dir=/mnt/models, --http_port=8080]
```

Built-in ClusterServingRuntimes: kserve-lgbserver (LightGBM), kserve-mlserver (SKLearn, XGBoost, LightGBM, MLflow), kserve-paddleserver, kserve-pmmlserver, kserve-sklearnserver, kserve-tensorflow-serving, kserve-tritonserver (TensorFlow, ONNX, PyTorch, TensorRT), kserve-xgbserver, kserve-huggingfaceserver.

Spec fields: `multiModel` (ModelMesh, default false), `disabled`, `containers[]` (image, command, args, resources, env, probes, workingDir), `supportedModelFormats[]` (name, version, autoSelect, priority), `storageHelper.disabled`, `nodeSelector`, `affinity`, `tolerations`. Use only the major version in `version` (for example "1").

Template variables like `{{.Name}}` map to InferenceService metadata; built-ins pass `--model_name={{.Name}}`.

Explicit use: set `runtime:` in the predictor. The controller searches the namespace first, then ClusterServingRuntimes, and checks `modelFormat` against `supportedModelFormats`. Pin `runtimeVersion` in production.

Legacy schema (`predictor.sklearn:`) is mutated by a webhook to the new `model.modelFormat` plus explicit runtime; the old ConfigMap-based predictor config was phased out in v0.10, and the page says the old schema will eventually be removed.

## Auto-selection and priority
Without `runtime`, the controller considers runtimes whose `supportedModelFormats` entry matches the format (and version, if given) with `autoSelect: true`. When several match, `priority` (greater than zero, higher wins, only used when `autoSelect` is true) decides. If no priority is set, which runtime is chosen is not guaranteed (the page says the most recently created one is selected), so enable `autoSelect` with care.

## Checked
Method: docs-only read of cited pages, 2026-11-08
Confirmed against the KServe website Serving Runtime page: scope difference, example, built-in runtimes, spec attributes, template variables, explicit and implicit selection, previous schema. Added the priority rules from the same page.
