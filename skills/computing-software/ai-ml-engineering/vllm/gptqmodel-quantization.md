---
id: computing-software.ai-ml-engineering.vllm.gptqmodel-quantization
name: gptqmodel-quantization
category: computing-software
field: ai-ml-engineering
product: vllm
tags: [gptqmodel, gptq, marlin, machete, dynamic-quantization]
level: practitioner
status: docs-checked
description: "Create and run 4-bit or 8-bit GPTQ models with GPTQModel, using Marlin and Machete kernels on Ampere and Hopper."
sources:
  - https://docs.vllm.ai/en/latest/features/quantization/gptqmodel/
  - https://docs.vllm.ai/en/latest/features/quantization/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: quantize to INT4 or INT8 GPTQ and serve with fast kernels.

GPTQModel (from ModelCloud.AI) reduces precision from BF16/FP16 to INT4 or INT8, cutting memory while increasing inference performance. Compatible models can use the `Marlin` and `Machete` vLLM custom kernels for batched throughput and token latency on Ampere (A100+) and Hopper (H100+) GPUs.

Distinctive feature: `Dynamic` per-module quantization, where different layers or modules get custom quantization parameters. It is fully integrated into vLLM; see the GPTQModel readme section "Dynamic quantization (per-module QuantizeConfig override)".

Install, or pick one of the 5000+ GPTQ models on Hugging Face:

```bash
pip install -U gptqmodel --no-build-isolation -v
```

Example flow for `meta-llama/Llama-3.2-1B-Instruct`: load a calibration set (`allenai/c4`, file `en/c4-train.00001-of-01024.json.gz`, first 1024 samples), build a `QuantizeConfig`, then load, quantize and save with the GPTQModel API (see the GPTQModel readme for details).

Serve a quantized model directly through the `LLM` entrypoint, for example:

```python
llm = LLM(model="ModelCloud/DeepSeek-R1-Distill-Qwen-7B-gptqmodel-4bit-vortex-v2")
sampling_params = SamplingParams(temperature=0.6, top_p=0.9)
```

Hardware per the overview: GPTQ runs on Volta through Hopper, Intel GPUs and x86 CPUs, not AMD GPUs.

## Checked

Method: 2026-11-08 read the GPTQModel page and the quantization overview in full. Kernel, dynamic quantization, install, example flow and hardware row matched; unchanged.
