---
id: computing-software.ai-ml-engineering.llama-cpp.server-prompt-cache-flags
name: server-prompt-cache-flags
category: computing-software
field: ai-ml-engineering
product: llama-cpp
tags: [llama-cpp, prompt-cache, cache-reuse, cache-ram, context-checkpoints]
level: advanced
status: docs-checked
description: "Tune llama-server prompt caching with cache-prompt, cache-reuse, cache-ram, checkpoints and slot similarity."
sources: ["https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Prompt caching flags

- `--cache-prompt` / `--no-cache-prompt` (default enabled): reuse the KV cache from a previous request; only the differing suffix is processed. Because logits are not guaranteed bit-identical across batch sizes, enabling it can make results nondeterministic. Per-request override: `cache_prompt`.
- `--cache-reuse N` (default 0): minimum chunk size to try reusing from the cache by KV shifting; requires prompt caching. Per-request: `n_cache_reuse`.
- `-cram, --cache-ram N`: maximum prompt cache size in MiB. Default 8192; `-1` is no limit; `0` disables.
- `--cache-idle-slots` (default enabled, needs cache-ram): saves idle slots to the prompt cache when a new task arrives and clears them when using a unified KV buffer.
- `-ctxcp, --ctx-checkpoints N`: maximum context checkpoints per slot (default 32).
- `-cms, --checkpoint-min-step N`: minimum token spacing between checkpoints (default 8192; 0 means no minimum).
- `-sps, --slot-prompt-similarity F`: how closely a request prompt must match a slot's prompt to use that slot (default 0.10; 0.0 disables).
- `--context-shift` (default disabled): shift the context on infinite generation.
- `--swa-full`: use a full-size SWA cache.

Check effect in responses: `tokens_cached` on `/completion`, or `timings.cache_n` and `usage.prompt_tokens_details.cached_tokens` on the chat route.

## Checked

2026-11-08. Confirmed in the llama.cpp server README: every flag, default and per-request field named above (cache_prompt, n_cache_reuse), the nondeterminism note, tokens_cached on /completion, timings.cache_n and usage.prompt_tokens_details.cached_tokens. Nothing removed.

Method: docs-only read of cited pages, 2026-11-08
