---
id: computing-software.ai-ml-engineering.llm-application-engineering.llm-latency-optimization
name: llm-latency-optimization
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, latency-optimization, ttft, streaming, prompt-caching, parallel-calls]
level: practitioner
status: docs-checked
description: "Cut LLM response latency: measure TTFT and total time, pick a faster model or lower effort, shorten prompts and outputs, stream and cache prompts."
sources:
  - https://docs.claude.com/en/docs/test-and-evaluate/strengthen-guardrails/reduce-latency
  - https://platform.openai.com/docs/guides/latency-optimization
  - https://docs.claude.com/en/docs/build-with-claude/prompt-caching
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Latency levers

**Goal:** users get responses within the product's latency budget, by attacking the parts of latency that actually dominate.

## Measure first
- **TTFT** (time to first token): time from sending the prompt to the first generated token; matters most with streaming.
- **Output time:** output tokens / tokens-per-second.
- **Pipeline overhead:** retrieval, tool calls, sequential LLM calls, network.
Log per request: input tokens, output tokens, TTFT, total, model, cache read tokens. Look at p95, not averages.

## Levers
First get a prompt that works well, then reduce latency; doing it too early hides what top quality looks like.
1. **Fewer output tokens:** ask for concise answers (paragraph or sentence limits work better than word counts) and set `max_tokens` as a hard cap. Hitting the cap cuts the response off, so it suits short answers.
2. **Right model and effort:** Anthropic's guide points to Claude Haiku 5.5 (`claude-haiku-5-5`) for speed-critical apps, with `output_config={"effort": "low"}` as the fastest and cheapest level. Measure quality at each level.
3. **Streaming:** perceived latency drops to TTFT; render as tokens arrive.
4. **Prompt caching:** you generally see improved time-to-first-token for long documents; the 5-minute and 1-hour caches behave the same for latency.
5. **Shorter inputs:** trim irrelevant context and history; be clear but concise.
6. **UX:** show progress for unavoidable waits.

## Checked
2026-11-01. Confirmed against Anthropic's Reducing latency guide (TTFT, Haiku 5.5 at low effort example, max_tokens, paragraph/sentence limits, streaming) and the prompt caching page (long-document TTFT, cache TTLs behave the same for latency). Removed: fast mode, regions, dedicated capacity, impact ordering, parallelism and agent advice. The OpenAI page was not used for any claim.
Method: documentation only; no commands were run.

## Verify
- [ ] Latency breakdown (TTFT, output, overhead) dashboarded per route.
- [ ] Each change measured on p95 with quality checked on the eval set.
