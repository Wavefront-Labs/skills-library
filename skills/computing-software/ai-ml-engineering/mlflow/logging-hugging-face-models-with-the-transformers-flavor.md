---
id: computing-software.ai-ml-engineering.mlflow.logging-hugging-face-models-with-the-transformers-flavor
name: logging-hugging-face-models-with-the-transformers-flavor
category: computing-software
field: ai-ml-engineering
product: mlflow
tags: [mlflow, mlflow-transformers-flavor, transformers, peft, llm-logging, model-signature]
level: practitioner
status: docs-checked
description: "Log Hugging Face pipelines and PEFT adapters with mlflow.transformers: task and signature choice, reference-only saving for large weights, loading as pipeline or pyfunc."
sources:
  - https://mlflow.org/docs/latest/ml/deep-learning/transformers/guide/
  - https://mlflow.org/docs/latest/ml/deep-learning/transformers/large-models/
  - https://github.com/mlflow/mlflow/blob/master/mlflow/transformers/__init__.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Transformers flavor (pipelines, PEFT, task)

**Goal:** a fine-tuned or off-the-shelf Hugging Face model is logged once and loads identically for notebooks (native pipeline) and serving (pyfunc), without copying 30 GB of weights per run.

## Log a pipeline
```python
import mlflow, transformers
pipe = transformers.pipeline("text-classification", model=model, tokenizer=tok)
with mlflow.start_run():
    info = mlflow.transformers.log_model(
        transformers_model=pipe,            # or {"model": model, "tokenizer": tok}
        name="classifier",                  # artifact_path on MLflow 2.x
        input_example=["refund not received"],
        registered_model_name="support-intent",
    )
```
The signature is inferred from the pipeline task; `input_example` adds a concrete example to the model page and validates the signature.

## Task and inference defaults
`task` is the transformers task string; if omitted, the transformers pipeline utilities infer it, and an unsupported value raises. `llm/v1/xxx` task strings are accepted and MLflow falls back to the matching default pipeline task for them. Inference defaults (for example `max_new_tokens`, `temperature`) go in `model_config={...}`; they apply when the model is loaded as pyfunc or used in Spark, not to a pipeline returned by `mlflow.transformers.load_model`. Callers can override them at `predict()` time only if the saved `ModelSignature` declares the same params. A key that is not valid for the pipeline raises at runtime, so validate `model_config` before logging.

## Large weights
`save_pretrained=False` (added in MLflow 2.11.0) stores the Hugging Face Hub repository name and the commit hash of the weights instead of copying them. Faster logging and less storage, but loading downloads from the Hub or uses the local Hugging Face cache, so it needs access (or a cache) and the commit to still exist; private or air-gapped serving needs the default `save_pretrained=True`.

## PEFT adapters
MLflow detects PEFT models when you log a pipeline whose model is a `PeftModel`. Set `base_model_path` to a local directory holding the base weights and only the adapter weights are saved; at load time the base model is read from that path and the adapter applied on top, so the path must be valid at both save and load time (useful for air-gapped environments and to avoid duplicating large weights). To serve without PEFT at runtime, merge the adapter into the base model before logging.

## Load
```python
pipe = mlflow.transformers.load_model(info.model_uri, device=0)                       # native pipeline
parts = mlflow.transformers.load_model(info.model_uri, return_type="components")   # dict of model/tokenizer
pyf = mlflow.pyfunc.load_model(info.model_uri)                                      # serving interface
```
`torch_dtype` (e.g. `torch.bfloat16`) at log time sets the dtype applied when the model is loaded back; if unspecified, the model instance's current dtype is used.

## Gotchas
- Serving images must use the library versions in the model's logged `requirements.txt`.
- Models with custom code (`trust_remote_code=True`) need `transformers >= 4.26.0` to be saved and the code available at load; prefer `models-from-code` or a pyfunc wrapper.
- Log the tokenizer you fine-tuned with, not a fresh one.

## Verify
- [ ] `mlflow models predict -m <uri> -i sample.json -t json` returns the same labels as the notebook pipeline.
- [ ] Logged artifact size matches expectations (adapter-only or reference-only where intended).

## Checked

- Date: 2026-10-25. Release: MLflow 3.17.2 (released 2026-10-20); documentation and source read from the master branch of mlflow/mlflow (docs/docs, mlflow/, CHANGELOG.md) on 2026-10-25.
- `mlflow.transformers.log_model` parameters (`transformers_model`, `task`, `torch_dtype`, `model_config`, `save_pretrained`, `base_model_path`, `name`, `artifact_path`, `input_example`, `registered_model_name`) and `load_model(model_uri, return_type='pipeline'|'components', device=...)`: mlflow/transformers/__init__.py.
- `model_config` semantics (pyfunc/Spark only, signature params override at predict) and `trust_remote_code` needing transformers >= 4.26.0: docs/classic-ml/deep-learning/transformers/guide/index.mdx.
- `save_pretrained=False` stores repo name and commit hash, introduced in 2.11.0: transformers/large-models/index.mdx. `base_model_path` PEFT behaviour: `save_model` docstring.
- `mlflow models predict -i ... -t json` flags (`--input-path`, `--content-type` json|csv): mlflow/models/cli.py.
- Removed as unconfirmed: the `llm/v1/chat` OpenAI-payload and Databricks/AI Gateway expectations, the fp32 memory-doubling claim, tokenizer chat-template statement and megabyte-sized adapter claim.

Method: documentation only; no commands were run.
