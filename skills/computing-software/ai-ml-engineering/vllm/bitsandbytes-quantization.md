---
id: computing-software.ai-ml-engineering.vllm.bitsandbytes-quantization
name: bitsandbytes-quantization
category: computing-software
field: ai-ml-engineering
product: vllm
tags: [bitsandbytes, vllm-bnb-plugin, inflight-quantization, 4-bit, bnb]
level: practitioner
status: docs-checked
description: "Use BitsAndBytes through the vllm-bnb-plugin for pre-quantized checkpoints or in-flight 4-bit quantization."
sources:
  - https://docs.vllm.ai/en/latest/features/quantization/bnb/
  - https://docs.vllm.ai/en/latest/features/quantization/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: cut memory use with BitsAndBytes without a calibration dataset.

BitsAndBytes quantizes models to reduce memory usage and enhance performance without significantly sacrificing accuracy. Compared with other methods it eliminates the need to calibrate the quantized model with input data. Support comes from the out-of-tree plugin `vllm-bnb-plugin`; install it first:

```bash
uv pip install vllm-bnb-plugin
```

vLLM reads the model's config file and supports both in-flight quantization and pre-quantized checkpoints. Pre-quantized repositories on Hugging Face usually have a `quantization_config` section in `config.json`.

Pre-quantized checkpoint: vLLM infers the method from the config, so you do not pass the quantization argument.

```python
llm = LLM(model="unsloth/tinyllama-bnb-4bit", dtype=torch.bfloat16, trust_remote_code=True)
```

In-flight 4-bit quantization: specify the argument explicitly.

```python
llm = LLM(model="huggyllama/llama-7b", dtype=torch.bfloat16,
          trust_remote_code=True, quantization="bitsandbytes")
```

OpenAI-compatible server: append `--quantization bitsandbytes` to the model arguments for in-flight 4-bit quantization.

Hardware per the quantization overview table: bitsandbytes runs on Volta through Hopper NVIDIA GPUs; the table marks AMD, Intel GPU and CPUs as unsupported.

## Checked

Method: 2026-11-08 read the BitsAndBytes page and the quantization overview page in full; plugin install, checkpoint inference, in-flight flag and hardware row all matched. No claims changed.
