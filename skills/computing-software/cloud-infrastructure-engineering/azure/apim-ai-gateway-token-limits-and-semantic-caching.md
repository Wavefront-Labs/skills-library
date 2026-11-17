---
id: computing-software.cloud-infrastructure-engineering.azure.apim-ai-gateway-token-limits-and-semantic-caching
name: apim-ai-gateway-token-limits-and-semantic-caching
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, api-management, ai-gateway, azure-openai-token-limit, llm-token-limit, semantic-caching, load-balancing]
level: advanced
status: docs-checked
description: "Front Azure OpenAI and other LLM endpoints with APIM AI gateway policies: token rate limits, token metrics, semantic caching, backend pools and managed identity auth."
sources: ["https://learn.microsoft.com/azure/api-management/genai-gateway-capabilities", "https://learn.microsoft.com/azure/api-management/llm-token-limit-policy", "https://learn.microsoft.com/azure/api-management/llm-emit-token-metric-policy", "https://learn.microsoft.com/azure/api-management/llm-semantic-cache-lookup-policy", "https://learn.microsoft.com/azure/api-management/backends"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# APIM AI gateway for language model APIs

**Goal:** share LLM capacity safely across apps: per-consumer token quotas, cost visibility, caching and failover.

## Import
Import the model API into API Management (portal wizards exist for Azure OpenAI and other language model APIs). For Azure OpenAI APIs imported from Microsoft Foundry, authentication with the instance's managed identity is configured automatically; for an API imported from an OpenAPI specification you configure authentication yourself.

## Auth to the backend with managed identity
```xml
<authentication-managed-identity resource="https://cognitiveservices.azure.com" output-token-variable-name="t" ignore-error="false" />
<set-header name="Authorization" exists-action="override"><value>@("Bearer " + (string)context.Variables["t"])</value></set-header>
```
Grant the APIM managed identity an appropriate data-plane role on each Azure OpenAI resource (check the Azure OpenAI role list for the exact role name) and remove API keys from clients.

## Token limit per consumer
```xml
<llm-token-limit counter-key="@(context.Subscription.Id)"
    tokens-per-minute="20000" estimate-prompt-tokens="true"
    remaining-tokens-header-name="x-remaining-tokens" />
```
`llm-token-limit` is the current policy for language model APIs. Exceeding the `tokens-per-minute` rate returns `429 Too Many Requests` (with a `Retry-After` header); exceeding a `token-quota` over a `token-quota-period` (Hourly, Daily, Weekly, Monthly or Yearly) returns `403 Forbidden`. Either a rate limit, a quota, or both must be set.

## Token metrics for chargeback
```xml
<llm-emit-token-metric namespace="llm">
  <dimension name="API ID" />
</llm-emit-token-metric>
```
The policy sends custom metrics to Application Insights; up to five custom dimensions are allowed. Some models, especially when streaming, don't return token counts unless the request sets `include_usage` to `true`, and interrupted streams give inaccurate counts.

## Semantic caching
```xml
<!-- inbound -->
<llm-semantic-cache-lookup score-threshold="0.05" embeddings-backend-id="embeddings-backend" embeddings-backend-auth="system-assigned">
  <vary-by>@(context.Subscription.Id)</vary-by>
</llm-semantic-cache-lookup>
<!-- outbound -->
<llm-semantic-cache-store duration="120" />
```
The lookup policy needs a matching store policy and an external cache plus an embeddings backend; follow the "Enable semantic caching for LLM APIs" article for the prerequisites (it references Azure Managed Redis as a semantic cache). Use `vary-by` to partition cached responses.

## Load balancing and failover
Create a backend **pool** of several backends and use weighted, priority-based or round-robin distribution; add **circuit breaker** rules (for example a failure count of 3 over an interval with status code range 500-599, a trip duration and `acceptRetryAfter`). Azure OpenAI returns 429 with a `Retry-After` value that can be very large (for example one day), so Microsoft advises circuit breaker rules on Azure OpenAI backends. Point the API at the pool with `set-backend-service`.

## Verify
- [ ] Exceeding tokens-per-minute returns 429 and the remaining-tokens header reaches 0.
- [ ] Application Insights shows the token custom metrics with the expected dimensions.
- [ ] A semantically similar repeated prompt is served from the cache.

## Checked

2026-10-24, against MicrosoftDocs/azure-docs (api-management: genai-gateway-capabilities, llm-token-limit-policy, llm-emit-token-metric-policy, llm-semantic-cache-lookup-policy, llm-semantic-cache-store-policy, azure-openai-enable-semantic-caching, backends, authentication-managed-identity-policy, azure-openai-api-from-specification): policy names and attributes, 429 for rate limit and 403 for quota, five-dimension limit, include_usage note, vary-by, backend pools (weighted, priority, round robin), circuit breaker properties, Azure OpenAI large Retry-After caution. The azure-openai-* policy pages no longer exist in the docs repository, so the skill now uses the llm-* policies. Removed the unconfirmed Redis RediSearch requirement, the PTU priority advice, the Cognitive Services role name and the Client IP and Subscription ID dimensions.

Method: documentation only; no commands were run.
