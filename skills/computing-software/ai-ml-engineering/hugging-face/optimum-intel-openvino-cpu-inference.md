---
id: computing-software.ai-ml-engineering.hugging-face.optimum-intel-openvino-cpu-inference
name: optimum-intel-openvino-cpu-inference
category: computing-software
field: ai-ml-engineering
product: hugging-face
tags: [hugging-face, openvino, optimum-intel, cpu-inference, int8-quantization, weight-compression, intel]
level: practitioner
status: docs-checked
description: "Speed up Hugging Face models on Intel CPUs and GPUs with Optimum Intel and OpenVINO: OVModel export, default 8-bit weights, OVQuantizer static quantization, GPU and static shapes."
sources:
  - https://huggingface.co/docs/optimum-intel/openvino/inference
  - https://huggingface.co/docs/optimum-intel/openvino/optimization
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# CPU inference with Optimum Intel / OpenVINO

## Export and run
```python
from optimum.intel import OVModelForSequenceClassification
from transformers import AutoTokenizer, pipeline
m = OVModelForSequenceClassification.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english", export=True)
m.save_pretrained("ov_sst2")                      # OpenVINO IR + config
tok = AutoTokenizer.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
clf = pipeline("text-classification", model=m, tokenizer=tok)
```
`export=True` converts a Transformers checkpoint to OpenVINO; reload an already-exported model without it.

## Compression
- Weight-only 8-bit: when a model larger than 1 billion parameters is exported with `export=True`, `load_in_8bit` defaults to True; disable with `load_in_8bit=False`.
- Static quantization of weights and activations uses `OVQuantizer` with a calibration dataset:
```python
from optimum.intel import OVQuantizer, OVConfig, OVQuantizationConfig
q = OVQuantizer.from_pretrained(model)
q.quantize(calibration_dataset=calib, save_directory="ov_int8", ov_config=OVConfig(quantization_config=OVQuantizationConfig()))
```

## Device and static shapes
- Pass `device="gpu"` (with an `ov_config` dict if needed) to `from_pretrained` to run on an Intel GPU.
- Models are compiled when instantiated. Dynamic shapes are the default; for static shapes call `model.reshape(batch_size, seq_len)`, after which inputs of another shape fail. After reshaping or changing device the model recompiles before first inference; set `compile=False` to skip the first compilation.

## Verify
Compare outputs/metrics vs the original model on a validation set, and compare end-to-end latency against PyTorch on the same machine.

## Checked
2026-11-01. Confirmed against the Optimum Intel OpenVINO inference and optimization pages: `export=True`, `load_in_8bit` default above 1 billion parameters, `OVQuantizer`/`OVConfig`/`OVQuantizationConfig` flow, `device="gpu"`, `reshape()` static shapes, `compile=False`. Removed (not confirmed on the pages read): install line, `optimum-cli` weight-format table and INT4 flags, "2-4x faster" figure, NPU and `PERFORMANCE_HINT` guidance, `benchmark_app` command, class-list and `generate()` remarks, IR forward-compatibility note.
Method: documentation only; no commands were run.
