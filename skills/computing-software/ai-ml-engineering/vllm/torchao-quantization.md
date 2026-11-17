---
id: computing-software.ai-ml-engineering.vllm.torchao-quantization
name: torchao-quantization
category: computing-software
field: ai-ml-engineering
product: vllm
tags: [torchao, int8-weight-only, transformers, torch-compile]
level: intro
status: docs-checked
description: "Quantize a Hugging Face model with TorchAO (Int8WeightOnlyConfig) and push it for use with vLLM."
sources:
  - https://docs.vllm.ai/en/latest/features/quantization/torchao/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: produce a TorchAO-quantized checkpoint that vLLM can load.

TorchAO is an architecture optimization library for PyTorch providing high-performance dtypes, optimization techniques and kernels for inference and training. It composes with native PyTorch features such as torch.compile and FSDP.

The docs recommend the latest TorchAO nightly build, choosing the CUDA suffix (`cu126`, `cu128`, ...) that matches your system:

```bash
pip install --pre torchao>=10.0.0 \
    --index-url https://download.pytorch.org/whl/nightly/cu126
```

Quantizing a Hugging Face model with transformers (diffusers also supports TorchAO) and saving to the Hub:

```python
from transformers import TorchAoConfig, AutoModelForCausalLM, AutoTokenizer
from torchao.quantization import Int8WeightOnlyConfig

quantization_config = TorchAoConfig(Int8WeightOnlyConfig())
quantized_model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Meta-Llama-3-8B",
    dtype="auto", device_map="auto",
    quantization_config=quantization_config,
)
tokenizer.push_to_hub(hub_repo)
quantized_model.push_to_hub(hub_repo, safe_serialization=False)
```

Note the example pushes with `safe_serialization=False`. The page links an example checkpoint published this way and a Hugging Face space ("TorchAO Quantization") for quantizing models through a simple UI.

Benchmark numbers are linked from the page (pytorch/ao repository, torchao/quantization benchmarks). The example Hub checkpoint it links is `jerryzh168/llama3-8b-int8wo`, an int8 weight-only Llama 3 8B.

## Checked

Method: 2026-11-08 read the TorchAO page in full. Install note, Int8WeightOnlyConfig example, safe_serialization=False and linked checkpoint matched; unchanged. The page itself does not show loading the result in vLLM, only producing the checkpoint.
