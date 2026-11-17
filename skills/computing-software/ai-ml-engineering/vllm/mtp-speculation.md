---
id: computing-software.ai-ml-engineering.vllm.mtp-speculation
name: mtp-speculation
category: computing-software
field: ai-ml-engineering
product: vllm
tags: [mtp, multi-token-prediction, gemma-4, speculative-decoding-mtp]
level: practitioner
status: docs-checked
description: "Use method mtp for target models with native multi-token prediction, including Gemma 4 assistant checkpoints."
sources:
  - https://docs.vllm.ai/en/latest/features/speculative_decoding/mtp/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: speculative decoding with no separate draft model when the target has native multi-token prediction.

Use MTP when your model natively supports it and you want model-based speculation with minimal configuration. It only works for model families that support MTP in vLLM; otherwise use EAGLE or draft-model speculation.

Offline example from the page:

```python
llm = LLM(
    model="XiaomiMiMo/MiMo-7B-Base",
    tensor_parallel_size=1,
    speculative_config={"method": "mtp", "num_speculative_tokens": 1},
)
```

Online: `vllm serve XiaomiMiMo/MiMo-7B-Base --tensor-parallel-size 1 --speculative-config '{"method":"mtp","num_speculative_tokens":1}'`.

`num_speculative_tokens` sets speculative depth; the page suggests a small value like 1 as a starting point.

Gemma 4 assistant models are handled by vLLM's Gemma 4 MTP path, not as generic draft models, even though the checkpoint goes in the `model` field:

```bash
vllm serve google/gemma-4-E2B-it --tensor-parallel-size 1 --max-model-len 8192 \
  --speculative-config '{"method":"mtp","model":"gg-hf-am/gemma-4-E2B-it-assistant","num_speculative_tokens":1}'
```

Supported assistants: E2B, E4B, 12B, 26B-A4B and 31B Gemma 4 IT. Tower-based variants use `model_type: gemma4_assistant`; the encoder-free Gemma 4 Unified 12B uses `gemma4_unified_assistant`. Both map to `Gemma4MTPModel`, with the assistant layers sharing KV cache with the target.

If startup logs show `SpeculativeConfig(method='draft_model', ...)` for a Gemma 4 assistant, your release lacks Gemma 4 MTP support and may fail initializing multimodal Gemma 4 targets; upgrade rather than force it as a draft model.

Quantized drafter head: when the MTP head shares the target's unquantized lm_head (most MTP models), `"draft_lm_head_quantization": "fp8"` or `"nvfp4"` in `--speculative-config` gives the drafter a quantized copy (Model Runner V2). The target still verifies with its own head, so outputs are unchanged and only acceptance length can move. The copy costs about 1 byte (FP8) or 0.56 bytes (NVFP4) per lm_head weight, counted in model weights, so leave room for it when using `--kv-cache-memory-bytes`.

## Checked

Method: 2026-11-08 read the cited MTP page (vLLM docs source) in full and compared claim by claim. Core examples, Gemma 4 section and the upgrade warning were unchanged and correct. Added the Notes content (supported-families limit, depth default advice, draft_lm_head_quantization) that the draft omitted.
