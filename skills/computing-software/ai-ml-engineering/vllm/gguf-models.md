---
id: computing-software.ai-ml-engineering.vllm.gguf-models
name: gguf-models
category: computing-software
field: ai-ml-engineering
product: vllm
tags: [gguf, vllm-gguf-plugin, repo-id-quant-type, hf-config-path, tokenizer]
level: practitioner
status: docs-checked
description: "Serve GGUF checkpoints through vllm-gguf-plugin using repo_id:quant_type, base-model tokenizer and hf-config-path."
sources:
  - https://docs.vllm.ai/en/latest/features/quantization/gguf/
  - https://docs.vllm.ai/en/latest/features/quantization/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: load a GGUF quantized model in vLLM.

Warnings: GGUF support is highly experimental and under-optimized, may be incompatible with other features, and is for now a way to reduce memory footprint. Support migrated to the out-of-tree plugin; install it before serving:

```bash
uv pip install vllm-gguf-plugin
```

Load directly from Hugging Face with `repo_id:quant_type`:

```bash
vllm serve unsloth/Qwen3-0.6B-GGUF:Q4_K_M --tokenizer Qwen/Qwen3-0.6B
```

Add `--tensor-parallel-size 2` for two GPUs. A local file also works: download `Qwen3-0.6B-Q4_K_M.gguf` and run `vllm serve ./Qwen3-0.6B-Q4_K_M.gguf --tokenizer Qwen/Qwen3-0.6B`.

Always use the tokenizer from the base model: converting the tokenizer from GGUF is time-consuming and unstable, especially for large vocabularies.

GGUF assumes Hugging Face can convert its metadata into a config. If your model is not supported, supply a compatible config manually:

```bash
vllm serve unsloth/Qwen3-0.6B-GGUF:Q4_K_M \
   --tokenizer Qwen/Qwen3-0.6B --hf-config-path Qwen/Qwen3-0.6B
```

The `LLM` entrypoint accepts the same arguments (`model`, `tokenizer`). Hardware per the overview: Volta through Hopper NVIDIA and AMD GPUs.

## Checked

Method: 2026-11-08 read the GGUF page and the quantization overview in full. Warnings, plugin install, repo_id:quant_type, tokenizer advice, hf-config-path and hardware row matched; unchanged.
