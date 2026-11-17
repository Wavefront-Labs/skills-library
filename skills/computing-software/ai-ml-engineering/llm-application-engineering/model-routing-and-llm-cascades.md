---
id: computing-software.ai-ml-engineering.llm-application-engineering.model-routing-and-llm-cascades
name: model-routing-and-llm-cascades
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, model-routing, llm-cascade, cost-optimization, frugalgpt, fallback-models, difficulty-routing]
level: practitioner
status: docs-checked
description: "Cut LLM cost by routing requests: rule-based routes, learned difficulty routers, confidence-gated small-to-large cascades, error fallbacks, and evaluating the routed system."
sources:
  - https://arxiv.org/abs/2305.05176
  - https://arxiv.org/abs/2406.18665
  - https://platform.claude.com/docs/en/about-claude/models/choosing-a-model
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Model routing and LLM cascades

**Goal:** send each request to the cheapest model that handles it well, keeping overall quality near the strongest model.

## What the sources say
- **FrugalGPT (Chen, Zaharia, Zou, 2023):** LLM API fees can differ by two orders of magnitude. It outlines three cost strategies: prompt adaptation, LLM approximation and LLM cascade. FrugalGPT is a cascade that learns which combinations of LLMs to use for different queries; the authors report matching the best single LLM (for example GPT-4) with up to 98% cost reduction, or improving accuracy over GPT-4 by 4% at the same cost (their benchmarks, not your workload).
- **RouteLLM (Ong et al., 2024):** router models choose dynamically between a stronger and a weaker LLM at inference time, trained with human preference data plus data augmentation; they report cost cuts of over 2x in some cases without hurting response quality, and transfer to different strong/weak model pairs at test time.
- **Claude docs (Choosing the right model):** effort parameter tuning is often a better lever than switching models; multi-model strategies pair a lower-cost model with a frontier model, either as an executor that escalates hard decisions to an advisor or an orchestrator that delegates bulk work to lower-cost workers; the docs also describe efficiency-first and capability-first starting points and say a use-case-specific eval set is the most important step.

## Patterns (practitioner synthesis)
1. **Rule-based routing** by task type: classification and extraction to a small model; complex reasoning, long documents and code to a large model. Simple and predictable.
2. **Learned router:** a classifier predicts whether the small model will succeed. RouteLLM trains on preference data; with your own data, grade both models' outputs on your eval set and use "small model passed" as the label.
3. **Cascade:** call the small model first; accept the answer if a check passes (schema valid, verifier or judge score, calibrated confidence), otherwise escalate. Escalated requests pay both costs and add latency.
4. **Effort levels within one model** as a single-model alternative: lower effort for easy routes. Measure this before building a multi-model cascade.
5. **Fallbacks** for availability: on 429, 5xx or overload errors retry on another model or provider with a compatible prompt.

## Evaluate the routed system, not the parts (practitioner advice)
On a held-out set: overall quality, share routed to each model, cost per request, p95 latency. Plot the cost-quality curve as the routing threshold varies and pick the operating point explicitly. Re-collect router data when models change.

## Gotchas (practitioner advice)
- Prompts tuned for one model often underperform on another; keep per-model variants and test each.
- Prompt caches are per model, so splitting traffic lowers each model's hit rate.
- A weak cascade check lets bad small-model answers through silently.
- Monitor the routing distribution in production; traffic drift shifts cost.

## Verify
- [ ] Routed system's quality within an agreed margin of the all-large-model baseline.
- [ ] Cost and latency savings measured on real traffic.
- [ ] Fallback path tested by simulating provider errors.

## Checked
Method: docs-checked 2026-11-09 against the arXiv abstract pages for FrugalGPT (2305.05176) and RouteLLM (2406.18665) (full papers not read) and the Claude Choosing the right model page. Dropped: the OpenAI latency-optimization source (not read). Corrected: RouteLLM routers are trained on human preference data, not on graded outputs of both models. Patterns and gotchas are practitioner synthesis.
