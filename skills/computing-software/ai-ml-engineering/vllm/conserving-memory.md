---
id: computing-software.ai-ml-engineering.vllm.conserving-memory
name: conserving-memory
category: computing-software
field: ai-ml-engineering
product: vllm
tags: [conserving-memory, oom, enforce-eager, limit-mm-per-prompt, max-model-len]
level: practitioner
status: docs-checked
description: "Reduce GPU and CPU memory use with tensor parallelism, context limits, fewer CUDA graphs and multimodal limits."
sources:
  - https://docs.vllm.ai/en/latest/configuration/conserving_memory/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: stop out-of-memory failures when loading or running a large model.

Options from the guide, in order:
- Tensor parallelism: `LLM(model=..., tensor_parallel_size=2)` splits the model across GPUs. Do not call CUDA functions before creating `LLM` (error: `Cannot re-initialize CUDA in forked subprocess`); select devices with `CUDA_VISIBLE_DEVICES`. Each TP process reads the whole checkpoint, so load time grows with TP; convert to a sharded checkpoint with the repository's `load_sharded_state_offline.py` example to keep load time constant.
- Quantization: statically quantized models from the HF Hub work directly; dynamic quantization uses the `quantization` option.
- Limit `max_model_len` and `max_num_seqs`, for example `max_model_len=2048, max_num_seqs=2`.
- Fewer CUDA graphs: `compilation_config=CompilationConfig(mode=CompilationMode.VLLM_COMPILE, cudagraph_capture_sizes=[1, 2, 4, 8, 16])` (default goes up to `max_num_seqs`), or disable capture with `enforce_eager=True`.
- Sparse indexer on SM100: `VLLM_SPARSE_INDEXER_MAX_DECODE_LOGITS_MB` (default 2048; 0 disables chunking).

CPU RAM: `mm_processor_cache_gb` sets the multimodal cache (default 4 GiB); on the CPU backend `VLLM_CPU_KVCACHE_SPACE` sets KV cache in GiB (default 0, no override).

Multimodal limits: `limit_mm_per_prompt={"image": 3, "video": 1}`; set a modality to 0 (`{"video": 0}`) to allocate nothing for it.

## Checked

2026-11-03. Confirmed against the Conserving Memory page (docs.vllm.ai/en/latest/): tensor parallelism note, quantization, max_model_len/max_num_seqs, CUDA graph options, cache sizes and multimodal limits.

Method: documentation only; no commands were run.
