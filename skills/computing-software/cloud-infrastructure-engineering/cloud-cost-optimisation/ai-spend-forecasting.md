---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.ai-spend-forecasting
name: ai-spend-forecasting
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, ai-finops, forecasting, llm-costs, gpu-costs, token-pricing]
level: advanced
status: docs-checked
description: "Forecast AI spend per FinOps guidance: shorter windows, frequent revision, flexible pilot budgets, an AI scope, and anomaly watch for runaway usage."
sources: ["https://www.finops.org/wg/finops-for-ai-overview/", "https://www.finops.org/framework/capabilities/forecasting/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Forecasting AI token and GPU spend

The FinOps for AI overview says AI forecasts are less predictable than cloud forecasts, especially
early on. Adapt Forecasting with shorter windows and more frequent revisions, and use Budgeting to
agree flexible funding for pilots with Finance.

## Steps
1. **Define an AI Scope.** Model APIs, cloud services, SaaS and developer tools, GPUs and data
   centres can all feed one AI Scope; report AI as its own line.
2. **Allocate first.** Tag training separately from inference and production from experimentation;
   map each API key to one team, application and cost centre; use provider attribution or a proxy
   where tags are unsupported.
3. **Build the forecast model per the Framework**: base it on estimates, history and planned
   changes; document timing, implementation details, pricing models and when they apply, and the
   total cost of ownership. Owners keep the model current and seek funding when actuals exceed it.
4. **Choose the method by maturity**: Crawl is manual and based on history; Walk is rolling and
   trend-based with commitment discounts included; Run adds driver-based models and amortised,
   discount-adjusted tracking.
5. **Know the drivers**: pricing is volatile (models are repriced often, in either direction),
   capacity can be scarce in some regions, and spend can be driven by people far outside IT.
6. **Account for pricing model effects**: commitments and provisioned capacity, tier boundaries,
   and free tiers or previews that end.
7. **Watch for anomalies at application level**: runaway training jobs, agent loops, prompt changes
   that double token use and model switches that change price. Monitor tokens per minute, not just
   daily spend.
8. **Review forecast against actuals** and feed the variance back into the estimating method.

## Checked
Method: docs-checked 2026-11-09 against the FinOps for AI overview (fundamentals, best practices, maturity and KPI sections read) and the FinOps Framework Forecasting capability page (definition and maturity read).
Removed as unconfirmed: the monthly cost driver formula with cache and batch discount terms, p50 and p90 token sampling, 5 to 50x agent multipliers, 20 to 50 percent failed training run allowance, the claim that per-token prices have historically fallen, rate-limit and quota gotcha, and the Anthropic and Vertex pricing sources (unreadable).
