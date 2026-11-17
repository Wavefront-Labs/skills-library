---
id: computing-software.ai-ml-engineering.llm-application-engineering.llm-cost-modeling
name: llm-cost-modeling
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, llm-cost-modeling, token-pricing, unit-economics, prompt-caching, batch-api]
level: practitioner
status: docs-checked
description: "Model LLM feature costs from token prices: token profiles, cache read/write rates, batch discounts, agent loop multipliers, cost per task."
sources:
  - https://platform.claude.com/docs/en/about-claude/pricing
  - https://platform.claude.com/docs/en/build-with-claude/prompt-caching
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Cost modeling from token prices

## Per-request formula
`cost = (uncached_input x p_in) + (cache_write x p_write) + (cache_read x p_read) + (output x p_out)`
Example prices from the Claude pricing page at review time (per million tokens, check the page): `claude-opus-5-5` $4 in / $20 out (cache reads $0.20), `claude-sonnet-5-5` $2 / $10 (cache reads $0.10), `claude-haiku-5-5` $0.10 / $0.50 for prompts up to 100,000 tokens ($0.50 / $2.50 above that). Cache writes cost 1.25x base input for the 5-minute TTL and 2x for the 1-hour TTL; cache reads are 0.1x base input generally, but 0.05x on Opus 5.5 and Sonnet 5.5 (and 0.025x on Fable 5.1 and Mythos 5.1). Multipliers such as US-only inference (`inference_geo`, 1.1x) and the Batch API discount stack with these.

## Build a token profile
Measure from real logs (`usage` fields), not guesses: system prompt, tools, retrieved context, history, user input, output, thinking. Per route, take p50 and p95.

Worked example (support bot on `claude-sonnet-5-5`, 6 turns/conversation):
- 8k-token system + tools cached: first turn writes cache ($2.50/M), later turns read it ($0.10/M).
- Per turn: 2k new input, 400 output (history growth ignored for simplicity).
- Without caching: 6 x (10k x $2 + 0.4k x $10) / 1e6 = $0.144. With caching: turn 1 = (8k x $2.50 + 2k x $2 + 0.4k x $10) / 1e6 = $0.028; turns 2-6 = (8k x $0.10 + 2k x $2 + 0.4k x $10) / 1e6 = $0.0088 each; total ≈ $0.072.

## Multipliers
- Agent loops: each tool iteration resends the growing context; cost grows roughly quadratically with steps unless cached/compacted.
- Retries and fallbacks: add the observed retry rate.
- Batch API: 50% discount on both input and output tokens for asynchronous work.
- Long-context pricing tiers on some models above a token threshold (Haiku 5.5 above 100,000 tokens); Claude 4.6 and later models other than Haiku 5.5 include the 1M context window at standard pricing.

## Unit economics
Cost per **completed task** (successful resolution), not per request. Compare to the value or the human cost it replaces; model monthly spend = tasks/month x cost/task with growth scenarios.

## Levers (in order)
Caching and input hygiene, output length limits, batch for offline, effort tuning, smaller models for sub-tasks.

## Verify
- [ ] Forecast spreadsheet reconciled with one week of actual billing within ±15%.

## Checked
Method: docs-checked 2026-11-09 against the Claude pricing page (model price table, cache multipliers, batch and long-context sections, by keyword search) and the prompt-caching page (cache write multipliers). Corrected the worked example (Sonnet 5.5 cache reads are $0.10/M, total now about $0.072). Dropped: the claim that output includes thinking tokens (not confirmed on pages read) and the batch-processing source (not read). The quadratic agent-loop growth and the levers ordering are practitioner reasoning.
