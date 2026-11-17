---
id: computing-software.ai-ml-engineering.vllm.autoawq-quantization
name: autoawq-quantization
category: computing-software
field: ai-ml-engineering
product: vllm
tags: [awq, autoawq, auto-awq, quantization-auto-awq, 4-bit]
level: practitioner
status: docs-checked
description: "Run or create 4-bit AWQ models; note that AutoAWQ is deprecated in favour of llm-compressor."
sources:
  - https://docs.vllm.ai/en/latest/features/quantization/auto_awq/
  - https://docs.vllm.ai/en/latest/features/quantization/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: run 4-bit AWQ models, and know the library status.

Warning from the docs: the AutoAWQ library is deprecated. Its functionality was adopted by the vLLM project in `llm-compressor` (AWQ examples there are the recommended workflow).

AWQ reduces precision from BF16/FP16 to INT4, which shrinks the total model memory footprint; the main benefits are lower latency and lower memory usage. The docs link to AutoAWQ's own documentation for basic quantization details. You can quantize your own models or pick one of the 6500+ AWQ models on Hugging Face.

```bash
pip install autoawq
```

Quantization example for `mistralai/Mistral-7B-Instruct-v0.2` uses:

```python
quant_config = {"zero_point": True, "q_group_size": 128, "w_bit": 4, "version": "GEMM"}
model = AutoAWQForCausalLM.from_pretrained(model_path, low_cpu_mem_usage=True, use_cache=False)
model.quantize(tokenizer, quant_config=quant_config)
model.save_quantized(quant_path)
```

Run an AWQ model by naming the method:

```bash
python examples/deployment/llm_engine_example.py \
    --model TheBloke/Llama-2-7b-Chat-AWQ \
    --quantization auto_awq
```

Through the Python entrypoint: `LLM(model="TheBloke/Llama-2-7b-Chat-AWQ", quantization="auto_awq")` with `SamplingParams(temperature=0.8, top_p=0.95)`.

Hardware: per the quantization overview table, AWQ runs on Turing through Hopper GPUs, Intel GPUs and x86 CPUs, but not Volta or AMD GPUs.

## Checked

Method: 2026-11-08 read the AutoAWQ page and the quantization overview in full. Deprecation warning, install, quantize config, serve commands and the hardware row matched; unchanged.
