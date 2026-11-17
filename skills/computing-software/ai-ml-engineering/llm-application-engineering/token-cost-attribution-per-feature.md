---
id: computing-software.ai-ml-engineering.llm-application-engineering.token-cost-attribution-per-feature
name: token-cost-attribution-per-feature
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, llm-observability, token-cost-attribution, llm-finops, usage-api, unit-economics, cost-per-task]
level: practitioner
status: docs-checked
description: "Attribute LLM spend to features, customers and prompt versions: request tagging, cost from usage incl. cache tokens, provider usage APIs, cost per successful task."
sources:
  - https://platform.claude.com/docs/en/api/usage-cost-api
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Token cost attribution per feature

**Goal:** know what each feature, customer and prompt version costs, so you can price, optimise and catch runaway spend.

## Tag every request (practitioner advice)
Wrap the client so every call records: feature/route, prompt version, model, tenant/customer (pseudonymised), environment, and trace ID. Use separate API keys or workspaces per product area: Claude's usage reports can filter and group by API key, workspace, model, service tier, context window, data residency or speed, so spend splits without your logs.

## Compute cost from usage
```python
PRICES = load_price_table(version="2026-11")      # per model, per million tokens; versioned config
def request_cost(model, u):
    p = PRICES[model]
    return (u.input_tokens * p.input
            + getattr(u, "cache_creation_input_tokens", 0) * p.cache_write
            + getattr(u, "cache_read_input_tokens", 0) * p.cache_read
            + u.output_tokens * p.output) / 1e6
```
- Cache writes and reads are priced differently from plain input (see the prompt-caching and pricing pages); include batch discounts and tool/server-side charges where applicable.
- Keep the price table versioned; prices change and models are added.

## Reconcile with the provider's reports
Claude's Admin API provides `/v1/organizations/usage_report/messages` (token counts, filter and group by the dimensions above, `bucket_width` such as 1d or 1h, `group_by[]=model`) and `/v1/organizations/cost_report` (USD costs, grouped by `workspace_id` or `description`; grouping by description adds parsed fields such as model). Caveats from the docs:
- Both endpoints need Admin API credentials (an Admin API key, an `org:admin` OAuth token, or a personal or service-account key not scoped to a workspace); workspace API keys do not work, and the Admin API is unavailable for individual accounts.
- Priority Tier costs are not in the cost endpoint (track them via the usage endpoint's `service_tier`); code execution costs appear only in the cost endpoint.
- Console playground usage has a null `api_key_id`.
- These endpoints are labelled legacy: the docs recommend the newer Usage and Cost Analytics API for new integrations.
Reconcile monthly; a gap larger than a few percent suggests untagged traffic (practitioner threshold).

## Metrics that matter (practitioner advice)
- Cost per request by feature and model; p50/p95 tokens per request.
- **Cost per successful task** (divide by completed outcomes, including retries and agent loops), the unit that drives pricing decisions.
- Cost per active customer/tenant (heavy users, abuse).
- Cache hit rate and its savings.

## Alerts (practitioner advice)
Daily spend per feature vs forecast; sudden per-request token growth (history accumulation, prompt bloat after a deploy); a single tenant exceeding quota. Enforce per-tenant budgets in the gateway for multi-tenant products.

## Verify
- [ ] Most spend (target above 95%) attributable to a feature in your logs.
- [ ] Logged cost reconciles with the provider bill.
- [ ] Cost per successful task tracked for each major feature.

## Checked
Method: docs-checked 2026-11-09 against the Claude Usage and Cost API page (platform.claude.com, read through the cost endpoint and notes; the Analytics API page was not read). Dropped: the OpenAI usage, OpenTelemetry GenAI metrics and FinOps Foundation sources (not read) and the claim that reasoning tokens are billed as output (not on the page read). Tagging, metrics and alert sections are practitioner guidance.
