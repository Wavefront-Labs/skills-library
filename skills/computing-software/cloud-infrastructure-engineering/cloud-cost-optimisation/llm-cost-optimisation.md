---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.llm-cost-optimisation
name: llm-cost-optimisation
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, cost-aware-architecture, llm-cost-optimisation, prompt-caching, model-routing, batch-inference, token-budget, genai-finops]
level: advanced
status: draft
description: "Architect LLM applications for cost: token accounting, prompt caching, model routing/cascades, batch APIs, context trimming, response caching and per-feature unit costs."
sources: ["https://www.finops.org/wg/finops-for-ai-overview/", "https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching", "https://platform.openai.com/docs/guides/batch", "https://docs.aws.amazon.com/bedrock/latest/userguide/batch-inference.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# LLM cost architecture

## Cost drivers
Input tokens x price + output tokens x price (output usually several times dearer), per model
tier; plus embeddings, vector store, guardrail calls, and provisioned throughput if committed.

## Techniques (largest savings first, measure each)
1. **Right model per task**: route simple classification/extraction to small models; reserve large
   models for hard reasoning. Cascades: try small, escalate on low confidence.
2. **Prompt caching** for long, repeated prefixes (system prompts, documents, tool definitions):
   providers bill cached input tokens at a large discount; structure prompts with static content first.
3. **Batch APIs** for non-interactive workloads (typically ~50% discount, results within hours).
4. **Trim context**: retrieve fewer, better chunks; summarise conversation history; cap tool output size.
5. **Constrain output**: max tokens, concise formats, structured output instead of prose.
6. **Response caching** (exact or semantic) for repeated questions.
7. **Provisioned throughput / committed capacity** only when utilisation is high and steady.

## FinOps practices
- Log tokens (input, cached, output) per request with feature/tenant tags; build cost per feature
  and per user/tenant.
- Budgets and rate limits per API key/team; anomaly alerts on token spend.
- Evaluate quality alongside cost (an eval set) before switching models.

## Gotchas
- Agents looping with tools can multiply tokens per task; cap steps and total tokens.
- Caching invalidated by small changes early in the prompt (timestamps at the top).

## Verify
- [ ] Cost per successful task tracked; changes evaluated on quality and cost.
