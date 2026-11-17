---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.ai-cost-estimation
name: ai-cost-estimation
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, ai-finops, llm-costs, cost-estimation, token-pricing, gpu-costs]
level: practitioner
status: docs-checked
description: "Estimate AI workload cost the FinOps for AI way: understand pricing models and cost channels, baseline cost and quality, and include the full cost."
sources: ["https://www.finops.org/wg/finops-for-ai-overview/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Estimating AI / LLM workload cost

## Know the channels and units
| Channel | Typical cost unit |
|---|---|
| Direct model provider APIs | per token |
| Cloud provider model services | per token, call or hour, on the cloud bill |
| Model routers and aggregators | credits or per token |
| Embedded AI in SaaS and dev tools | per seat, add-on or usage |
| GPU providers for training and self-hosting | GPU hours, storage, networking |
| Owned or colocated infrastructure | capital, power and operating cost |

The tokens a user types are not always the tokens billed, because applications add system prompts,
history and retrieved content. Cost still equals price times quantity.

## Pricing models and what to watch
- On-demand: runaway usage without monitoring and limits.
- Commitment discounts: underused commitments when workloads change.
- Provisioned capacity: a fixed block billed whether used or not; low utilisation can cost more per
  token than on-demand, so model the break-even utilisation before buying.
- Spot, preemptible and batch: interruptions; needs scheduling and checkpointing.
- Subscription or seat: paying for unused seats.
- Tiered or volume: forecasting errors around tier boundaries.
- Free tier or preview: cost jumps when previews end or usage scales.

## Steps
1. **Estimate before building**, including the share of outputs that will not meet the quality bar.
2. **Set two baselines**: cost (from current invoices and usage) and functional (response time,
   accuracy, reliability, request volume).
3. **Choose the least expensive model that meets the quality bar** for each task; model choice is a
   cost and a quality decision at once.
4. **Include the full cost**: data stores, orchestration, observability and platform labour, not
   just tokens.
5. **Account for token efficiency levers**: prompt caching for stable prefixes and batch
   processing for non-urgent work.
6. **Present unit costs** (per inference, per user, per successful outcome) as distributions, since
   AI costs vary from run to run.
7. **Compare estimate with actuals** once running, using application-level token metering.

## Checked
Method: docs-checked 2026-11-09 against the FinOps for AI overview (fundamentals, pricing models, best practices and KPI sections read).
Removed as unconfirmed: the monthly cost formula, the claims that output tokens are priced several times input and batch is typically 50 percent off, agent loop multipliers of 5 to 20x, the self-hosted GPU formula, and the provider pricing page sources (Anthropic, Vertex AI and Bedrock pages unreadable).
