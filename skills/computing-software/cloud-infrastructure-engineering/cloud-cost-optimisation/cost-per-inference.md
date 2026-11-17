---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.cost-per-inference
name: cost-per-inference
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, unit-economics, cost-per-inference, ai-finops, llm-costs, cost-per-token, gpu-costs, unit-cost]
level: advanced
status: docs-checked
description: "Measure AI unit costs per FinOps for AI guidance: cost per inference, per million tokens and per successful outcome, with the formulas and the cautions."
sources: ["https://www.finops.org/wg/finops-for-ai-overview/", "https://www.finops.org/framework/capabilities/unit-economics/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cost per AI inference and per token

AI features need their own unit costs. The FinOps for AI overview recommends measuring the use
case, not the token: track cost per successful outcome and report it as a range, because AI costs
vary from run to run.

## KPIs (FinOps for AI overview)
| KPI | Formula |
|---|---|
| Cost per inference | Total inference cost / number of inference requests |
| Cost per million tokens | Total token cost / (tokens used / 1,000,000) |
| Cost per successful outcome | Total cost of all runs / runs that meet the quality bar |
| Cost per API call | Total API cost / number of API calls |
| Resource utilization efficiency | Used capacity / provisioned capacity (GPU or accelerator) |
| Cache hit rate | Cache reads / (cache reads + cache writes + uncached input) |
| Model fit | Requests on overqualified models / total requests |

## How to apply
1. Start with resource-efficiency metrics (cost per token) and expand toward outcome measures such
   as cost per assist, per agent action or per case deflected, so decision makers see what the
   token bought.
2. The tokens a user types are not always the tokens billed: applications add system prompts,
   history and retrieved content. Instrument the application to capture billed tokens.
3. New SKUs and direct model provider bills often lack native tagging, so allocation needs
   engineering instrumentation. Map each API key to one team, application and cost centre.
4. Include the full cost, not only tokens: data stores, orchestration, observability and platform
   labour.
5. Set a cost baseline from current invoices and a functional baseline (response time, accuracy,
   reliability, request volume); cost targets mean little without the quality they must preserve.
6. Tie unit costs to outcomes someone owns (a resolved ticket, a merged pull request) and bring
   Finance and the outcome owner in early: FinOps supplies the cost, the business owns the value
   claim.

## Cautions
- Model fit depends on a quality bar per task, set through evaluations Engineering and Product
  agree on.
- ROI is only as good as its inputs: decide which costs and benefits to include first.

## Checked
Method: docs-checked 2026-11-09 against the FinOps for AI overview (KPIs, value and best-practice sections read) and the FinOps Framework Unit Economics page.
Removed as unconfirmed: the SQL query, self-hosted cost-per-1k-token formula, per-request log schema, the Anthropic prompt-caching source (host not read), and the claim that retries are counted in cost per outcome.
