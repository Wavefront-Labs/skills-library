---
id: computing-software.ai-ml-engineering.llm-application-engineering.prompt-caching-breakpoints-and-hit-rate
name: prompt-caching-breakpoints-and-hit-rate
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, prompt-caching, cache-control, cache-hit-rate, llm-cost, claude-api, prefix-caching]
level: practitioner
status: docs-checked
description: "Cut LLM cost and latency with Claude prompt caching: stable-prefix ordering, cache_control breakpoints, TTLs, silent invalidators and measuring hit rate."
sources:
  - https://platform.claude.com/docs/en/build-with-claude/prompt-caching
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Prompt caching: breakpoints and hit rate

**Goal:** reuse the processed prefix of long prompts (system prompt, tool definitions, documents, conversation history) so repeated requests are cheaper and faster.

## How it works
Caches match on an exact **prefix**. The cache hierarchy is `tools`, then `system`, then `messages`; a change at one level invalidates that level and all later ones. Cache writes occur only at your breakpoint, and the hash is cumulative, so changing any block at or before a breakpoint gives a different hash. Order the prompt from most stable to most volatile and keep anything per-request after the last breakpoint.

## Claude
```python
resp = client.messages.create(
    model=MODEL, max_tokens=2048,
    system=[{"type": "text", "text": LONG_SYSTEM_PROMPT_AND_DOCS,
             "cache_control": {"type": "ephemeral"}}],            # breakpoint: cache everything up to here
    messages=history + [{"role": "user", "content": question}],
)
u = resp.usage
print(u.cache_creation_input_tokens, u.cache_read_input_tokens, u.input_tokens)
```
- Two modes: **automatic caching** (one top-level `cache_control` field; the breakpoint moves to the last cacheable block as a conversation grows, best for multi-turn chat) and **explicit breakpoints** on individual content blocks. Automatic caching uses one of the 4 breakpoint slots; with 4 explicit breakpoints already present the API returns 400, and a different TTL on the last block also returns 400.
- Up to 4 explicit breakpoints. On a read the system looks backward from the breakpoint for entries earlier requests wrote, but only 20 blocks back; if a growing conversation adds 20 or more blocks between writes, add a second breakpoint closer to that position.
- TTL: 5 minutes by default, refreshed at no extra cost on each use; `{"type": "ephemeral", "ttl": "1h"}` for longer gaps. A 5-minute write costs 1.25x base input price, a 1-hour write 2x, so the 1-hour option only pays off if gaps exceed 5 minutes. Breakpoints themselves add no cost.
- Cache reads are priced at a small fraction of base input (see the pricing page for the per-model multiplier).
- Prompts shorter than the model's minimum cacheable length (512 tokens on current 5.x models such as Opus 5.5, Sonnet 5.5 and Haiku 5.5; 1,024 to 4,096 on older ones) are processed without caching and no error is returned. If both `cache_creation_input_tokens` and `cache_read_input_tokens` are 0, the prompt was not cached.
- Place the breakpoint on the last block that stays identical across requests, i.e. the end of the static prefix, not on a block containing a timestamp or the incoming message (that gives a fresh write every request and no reads).

## Silent invalidators
- Timestamps, per-request context or the user message in or before the breakpoint block.
- Unstable key ordering in `tool_use` blocks: some languages (the docs name Swift and Go) randomise key order during JSON conversion, which breaks caches.
- Changes to `tool_choice`, to image presence anywhere in the prompt, to the thinking configuration or to `output_config.effort` between calls.
- Tool definitions changing per request (they are the first level of the hierarchy).

## Measure
`input_tokens` counts only tokens after the last breakpoint, so total input = `cache_read_input_tokens + cache_creation_input_tokens + input_tokens`. Hit rate = `cache_read_input_tokens / (input_tokens + cache_creation_input_tokens + cache_read_input_tokens)` over traffic. Track it per route on a dashboard; a sudden drop means a deploy introduced an invalidator.

## Verify
- [ ] Second identical-prefix request shows `cache_read_input_tokens` > 0.
- [ ] No volatile content before the last breakpoint (diff two requests' prefixes).
- [ ] Hit rate and cost per request tracked per route.

## Checked
Method: docs-checked 2026-11-09 against the Claude prompt-caching page (platform.claude.com, markdown version; automatic caching, breakpoints, pricing, minimum length, usage fields and troubleshooting sections read by keyword search). Dropped: the OpenAI and vLLM/SGLang paragraphs and sources (not read), and the "changing model" invalidator (not confirmed on that page).
