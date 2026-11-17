---
id: computing-software.ai-ml-engineering.hugging-face.kv-cache-types-and-static-cache
name: kv-cache-types-and-static-cache
category: computing-software
field: ai-ml-engineering
product: hugging-face
tags: [hugging-face, transformers, kv-cache, static-cache, torch-compile, generation-performance]
level: practitioner
status: gated
description: "Use transformers KV cache options: DynamicCache default, StaticCache for torch.compile, quantized and offloaded caches, cache reuse across turns, and memory sizing."
sources:
  - https://huggingface.co/docs/transformers/kv_cache
  - https://huggingface.co/docs/transformers/llm_optims
  - https://huggingface.co/docs/transformers/cache_explanation
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# KV cache types and static cache

During generation each layer stores keys and values for all previous tokens so each new token costs O(1) attention over cached states instead of recomputing the prefix.

## Size it
KV bytes ~ 2 x layers x kv_heads x head_dim x seq_len x batch x bytes_per_elem. Llama-3-8B (32 layers, 8 KV heads with GQA, head_dim 128; confirmed in the model's config.json via the NousResearch mirror) in bf16: 2 x 32 x 8 x 128 x 2 bytes = 131,072 bytes = 128 KiB per token, so 8k tokens x batch 8 = 8 GiB. Long contexts are often limited by KV cache, not weights.

## Cache types (`cache_implementation=` in generate or generation_config)
| Type | Use |
|---|---|
| `DynamicCache` (default) | grows per token; flexible; incompatible with full-graph compile |
| `"static"` (`StaticCache`) | preallocated to `max_cache_len`; fixed shapes allow `torch.compile` and CUDA graphs |
| `"offloaded"` / `"offloaded_static"` | keeps all but the current layer's cache on CPU (docs); long contexts on small GPUs, slower. Needs CUDA: on this CPU-only torch both raised `AssertionError: Torch not compiled with CUDA enabled` |
| `"quantized"` | KV quantised via `quanto` (default; int2/int4) or `hqq` (int1 to int8) per the kv_cache docs; needs `optimum-quanto` installed (ImportError otherwise); the docs warn it can hurt latency on short contexts. The "2-4x less memory" figure was not sourced and is removed |
| `"sliding_window"` / `"hybrid"` | `sliding_window` is deprecated and slated for removal in v5.13 (warning seen on 5.20.2): use `"static"` or `"offloaded_static"` and the layer structure (sliding or full) is inferred. All of `static`, `sliding_window`, `hybrid`, `dynamic` gave identical greedy output to the default on a tiny Llama |

## Static cache + compile (fast decode)
```python
out = model.generate(**inputs, max_new_tokens=256, cache_implementation="static")
# per the kv_cache docs, "static" also turns on automatic compilation of the decode stage
# (greedy and sampling); manual form:
# model.forward = torch.compile(model.forward, mode="reduce-overhead", fullgraph=True)
```
The static cache generated the same tokens as the default cache (ran on CPU). Compilation and the speedup were not run (no C compiler or GPU), so the "often 2-4x" figure is removed (gated: unconfirmed, source is paywalled or blocked). Keep batch size and max lengths fixed or bucketed to avoid recompiles; the docs note a static cache wastes attention compute on masked slots when sequence lengths vary a lot.

## Reuse cache across calls (multi-turn, shared prefix)
```python
from transformers import DynamicCache
prompt_cache = DynamicCache()
with torch.no_grad():
    prompt_cache = model(**tok(system_prompt, return_tensors="pt").to(model.device),
                         past_key_values=prompt_cache).past_key_values
cache = copy.deepcopy(prompt_cache)                        # don't mutate the shared prefix cache
out = model.generate(**tok(system_prompt + user_msg, return_tensors="pt").to(model.device),
                     past_key_values=cache, max_new_tokens=200)
```
Inputs must include the full text (prefix + new); generate skips the cached part. Ran on a tiny Llama: output equalled generation without the cache, the deep copy left the original prefix cache at 4 tokens while the copy grew to 13, and a plain forward returns a `DynamicCache` object.

## Gotchas
- `use_cache=False` (sometimes set for gradient checkpointing during training) makes generation quadratic: re-enable for inference (`model.config.use_cache = True`).
- The old tuple-of-tuples `past_key_values` format is gone from the outputs: a forward pass on 5.20.2 returns a `DynamicCache`; use Cache objects.
- Serving many concurrent requests: use vLLM/TGI (paged attention); transformers caches are per-call.

## Verify
Compare tokens/s and peak memory (`torch.cuda.max_memory_allocated`) for dynamic vs static vs quantized on your prompt lengths; outputs with greedy decoding should match between dynamic and static.
