---
id: computing-software.ai-ml-engineering.hugging-face.optimum-onnx-export-and-onnxruntime
name: optimum-onnx-export-and-onnxruntime
category: computing-software
field: ai-ml-engineering
product: hugging-face
tags: [hugging-face, optimum, optimum-onnx, onnx-export, onnxruntime, ortmodel, dynamic-quantization, cpu-inference]
level: practitioner
status: gated
description: "Export Transformers models to ONNX with Optimum, run them via ORTModel classes, apply graph optimization and dynamic int8 quantization, and validate numerics."
sources:
  - https://huggingface.co/docs/optimum/exporters/onnx/usage_guides/export_a_model
  - https://huggingface.co/docs/optimum/onnxruntime/usage_guides/models
  - https://huggingface.co/docs/optimum/onnxruntime/usage_guides/quantization
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Optimum ONNX export and ONNX Runtime inference

**Goal:** serve Transformers encoder (and small decoder) models faster on CPU or with ONNX Runtime GPU, without rewriting preprocessing.

## Export
```bash
pip install "optimum[onnxruntime]"      # optimum 2.1.0 pulls in the separate optimum-onnx 0.1.0 package, onnx and onnxruntime; it also pinned transformers to 4.57.6 and huggingface-hub to 0.36.2 in a venv that had transformers 5.20, so use a dedicated environment
optimum-cli export onnx --model distilbert-base-uncased-finetuned-sst-2-english --task text-classification onnx-sst2/
```
- `--task` selects the head and inputs/outputs (`feature-extraction`, `token-classification`, `text-generation-with-past` for decoders with KV cache).
- The exporter validates ONNX outputs against PyTorch within `--atol` (`--help`: "If specified, the absolute difference tolerance when validating the model. Otherwise, the default atol for the model will be used"); a validation failure means numerics differ - don't ignore it.
- Checked: the export above wrote `model.onnx` (268 MB, opset 18, inputs `input_ids` and `attention_mask` with dynamic `batch_size` and `sequence_length` axes) plus the tokenizer files and `config.json`.
- Opset can be set with `--opset`; newer ops need recent ONNX Runtime.

## Run with Transformers-like API
```python
from optimum.onnxruntime import ORTModelForSequenceClassification
from transformers import AutoTokenizer, pipeline
model = ORTModelForSequenceClassification.from_pretrained("onnx-sst2/")
# or export on the fly: from_pretrained(model_id, export=True)   (checked; it warns when the Hub repo already holds an ONNX file)
tok = AutoTokenizer.from_pretrained("onnx-sst2/")
clf = pipeline("text-classification", model=model, tokenizer=tok)
clf("ONNX Runtime is fast")
```
GPU: `provider="CUDAExecutionProvider"` (needs `onnxruntime-gpu`) (gated: unconfirmed, source is paywalled or blocked). No GPU was available here, and `onnxruntime.get_available_providers()` listed only `AzureExecutionProvider` and `CPUExecutionProvider`.

## Optimize and quantize
```python
from optimum.onnxruntime import ORTOptimizer, ORTQuantizer
from optimum.onnxruntime.configuration import OptimizationConfig, AutoQuantizationConfig
ORTOptimizer.from_pretrained(model).optimize(OptimizationConfig(optimization_level=2), save_dir="onnx-opt/")   # writes model_optimized.onnx
q = ORTQuantizer.from_pretrained("onnx-sst2/")          # quantize the plain export, see the note below
q.quantize(AutoQuantizationConfig.avx512_vnni(is_static=False, per_channel=False), save_dir="onnx-int8/")   # writes model_quantized.onnx
ORTModelForSequenceClassification.from_pretrained("onnx-int8/", file_name="model_quantized.onnx")   # non-standard file name needs file_name=
```
Checked with optimum 2.1.0, optimum-onnx 0.1.0 and onnxruntime 1.31 (CPU, dynamic quantization of the DistilBERT SST-2 export):
- Quantizing the **optimizer output** failed for `optimization_level=1` and `2` with `RuntimeError: Unable to find data type for weight_name=...MatMul_output_0 ... shape_inference failed`, so the earlier optimize-then-quantize chain does not work here; quantize the plain export (it worked) or compare the optimized model on its own.
- Optimization at level 2 left the file the same size (268 MB); dynamic int8 shrank it to 67 MB.
- Latency on this CPU (Intel family 6 model 151), batch of 8 short sentences, 20 timed runs: fp32 27.6 ms, int8 10.6 ms (about 2.6x); both predicted the same class for the sample. One machine, one model: measure your own.
- `AutoQuantizationConfig` offers `arm64`, `avx2`, `avx512`, `avx512_vnni`, `ppc64le` and `tensorrt` constructors.
- Dynamic int8 quantization on CPU gave a 4x smaller file and about 2.6x lower latency for this DistilBERT model (see above); accuracy loss was not measured here, so validate on your data. Match the config to the CPU's instruction set (`avx2`, `avx512`, `avx512_vnni`, `arm64`).
- Static quantization needs a calibration dataset; more speed, more risk.

## Gotchas
- Dynamic axes: the exporter sets batch and sequence dims dynamic (checked: batch of 2 with different lengths ran fine); fixed-shape exports break on other lengths.
- Tokenizer still runs in Python/Rust outside the ONNX graph; use the fast tokenizer and batch requests.
- Serving choice for long-sequence decoders (vLLM or TGI versus ONNX Runtime) was not tested here.

## Verify
- [ ] Exported model passes the exporter's validation.
- [ ] Accuracy of the int8 model on a validation set within tolerance.
- [ ] Latency/throughput measured vs PyTorch at your real batch sizes and sequence lengths.
