---
id: computing-software.cloud-infrastructure-engineering.azure.api-management-gateway-and-policies
name: api-management-gateway-and-policies
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, api-management, apim, api-gateway, apim-policies, policy-expressions, validate-jwt, rate-limit-by-key, quota, cache-lookup, set-backend-service, backends, circuit-breaker, load-balanced-backend, named-values, products, subscriptions, developer-portal, self-hosted-gateway, workspaces, apim-v2, internal-vnet, openapi-import, api-revisions, api-versions, apiops, apim-diagnostics, apim-logging]
level: advanced
status: docs-checked
description: "Run API Management as the API front door: tiers and VNet modes, OpenAPI import, revisions, policy pipeline (JWT, rate limits, caching), backends with circuit breaker, APIOps."
sources: ["https://learn.microsoft.com/en-us/azure/api-management/api-management-features", "https://learn.microsoft.com/en-us/azure/api-management/virtual-network-concepts", "https://learn.microsoft.com/en-us/azure/api-management/backends", "https://learn.microsoft.com/en-us/azure/api-management/validate-jwt-policy", "https://learn.microsoft.com/en-us/azure/api-management/rate-limit-by-key-policy", "https://learn.microsoft.com/en-us/azure/api-management/api-management-howto-properties", "https://learn.microsoft.com/en-us/cli/azure/apim", "https://github.com/Azure/apiops"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# API Management — one gateway, policies as code, backends that fail safely

**Goal:** every API published through APIM with consistent auth, throttling and
observability, and a policy set that lives in Git and deploys like code.

## 1. Tier and network
| Tier | Notes |
|---|---|
| Consumption | automatic scaling, no private endpoint, no VNet injection or backend-in-VNet connectivity, no resource logs, no backend circuit breaker |
| Developer | classic, no SLA, non-production; supports VNet injection, inbound private endpoint, self-hosted gateway (single node) |
| Basic / Basic v2 | Basic: inbound private endpoint; Basic v2: neither private endpoint nor VNet; Basic v2 supports workspaces |
| Standard / Standard v2 | private endpoint inbound; Standard v2 adds VNet **integration** (outbound to backends in a VNet) and workspaces; no VNet injection |
| Premium | VNet injection (internal/external), multi-region, availability zones, self-hosted gateway, workspaces |
| Premium v2 | VNet injection into a delegated subnet (gateway only) and private endpoint; no multi-region or self-hosted gateway |

Check the feature-comparison page for the current tier matrix before choosing.
```bash
az apim create -g rg -n apim-prod -l uksouth --sku-name Premium --sku-capacity 2 --publisher-email api@example.com --publisher-name Example \
  --virtual-network Internal --public-network-access false   # internal VNet mode: gateway/portal only on private IPs; front with App Gateway/Front Door
```
- Internal mode needs a dedicated subnet, NSG rules for inbound management traffic on port 3443 and outbound rules for the dependencies the VNet article lists (including Key Vault), and private DNS records for the gateway, portal, management and SCM hostnames. Front it with Application Gateway for external consumers.
- Custom domains + Key Vault certs with managed identity; gateway hostname `api.example.com`.
- Multi-region deployment is a Premium (classic) feature; the other tiers do not offer it.

## 2. APIs, products, subscriptions
```bash
az apim api import -g rg --service-name apim-prod --api-id orders --path orders --specification-format OpenApiJson --specification-url https://orders.internal/swagger/v1/swagger.json \
  --service-url https://orders.internal --protocols https --subscription-required true
az apim product create -g rg --service-name apim-prod --product-name Partners --product-id partners --subscription-required true --approval-required true --state published; az apim product api add -g rg --service-name apim-prod --product-id partners --api-id orders
az apim api release create -g rg --service-name apim-prod --api-id orders --api-revision 2 --notes "add /orders/{id}/cancel"   # revisions = non-breaking changes you can test before making current; versions (path/header/query string) = breaking, consumers choose
```
- **Subscription keys** (`Ocp-Apim-Subscription-Key`) for identification/metering, **JWT** for real auth — both. Products bundle APIs with their own quotas/terms; developer portal (customisable, Entra/B2C sign-in) publishes them.
- `--service-url` is the backend; better: a **backend** resource (`az apim backend create`) (`az apim backend create` requires `--backend-id`, `--protocol`, `--url`) and, for the circuit breaker and pool (below), the portal, REST API, Bicep or ARM, then `set-backend-service backend-id="orders-pool"`.

## 3. Policy pipeline (inbound → backend → outbound → on-error; global → product → API → operation with `<base/>`)
```xml
<policies>
  <inbound>
    <base />
    <validate-jwt header-name="Authorization" failed-validation-httpcode="401" require-scheme="Bearer">
      <openid-config url="https://login.microsoftonline.com/<tenant>/v2.0/.well-known/openid-configuration" />
      <audiences><audience>api://orders</audience></audiences>
      <required-claims><claim name="roles" match="any"><value>Orders.Read</value></claim></required-claims>
    </validate-jwt>
    <rate-limit-by-key calls="100" renewal-period="60" counter-key="@(context.Request.Headers.GetValueOrDefault("Ocp-Apim-Subscription-Key","anon"))" remaining-calls-header-name="X-RateLimit-Remaining" />
    <quota-by-key calls="100000" renewal-period="2592000" counter-key="@(context.Subscription?.Id ?? "anon")" />
    <cache-lookup vary-by-developer="false" vary-by-developer-groups="false" downstream-caching-type="none"><vary-by-header>Accept</vary-by-header></cache-lookup>
    <set-header name="X-Correlation-Id" exists-action="skip"><value>@(Guid.NewGuid().ToString())</value></set-header>
    <set-backend-service backend-id="orders-pool" />
    <authentication-managed-identity resource="api://orders-backend" />   <!-- APIM's identity → backend token; or client-cert / basic from named values -->
  </inbound>
  <backend><forward-request timeout="30" /></backend>
  <outbound><base /><cache-store duration="60" /><set-header name="Server" exists-action="delete" /></outbound>
  <on-error><base /><set-body>@(new JObject(new JProperty("error", context.LastError.Message)).ToString())</set-body></on-error>
</policies>
```
- Policy expressions are C# (`@(...)` single, `@{...}` multi-statement) with `context.Request/Response/Subscription/User/Variables`.
- Named values (`{{client-secret}}`) sourced from **Key Vault** (add them in the portal, Bicep or ARM; `az apim nv create` has `--secret` and `--value` but no Key Vault flag) — never literal secrets in policy. Key Vault secrets refresh into the named value within four hours; the instance's system-assigned identity is required when the Key Vault firewall is on.
- Other staples: `validate-azure-ad-token` (simpler Entra variant), `ip-filter`, `check-header`, `validate-content` (schema), `cors`, `rewrite-uri`, `mock-response`, `send-request`, `retry`, `limit-concurrency`, `llm-token-limit` for AI gateways, `return-response`.
- The v2 tiers use a token-bucket algorithm for `rate-limit-by-key`, classic tiers a sliding window, so identical settings behave differently across tiers.

## 4. Backends with resilience
```bash
az apim backend create -g rg --service-name apim-prod --backend-id orders-uks --url https://orders-uks.internal --protocol http
# the circuit breaker is a property of the backend resource (Bicep/ARM `circuitBreaker`, REST or portal), not an az apim backend create flag
```
When the breaker trips the gateway stops sending requests to the backend for the trip duration and returns 503; if a `Retry-After` header is present the breaker can honour it. One rule per backend; not supported on Consumption; rules are approximate because gateway instances do not synchronise. Pools spread load across backends in priority groups and fall to a lower priority group only when the higher group's breakers are tripped; pool load balancing is also approximate. Use `retry` with a `condition` for idempotent calls, and keep the `forward-request` timeout below the client's.

## 5. Observability and APIOps
- Diagnostic settings → `ApiManagementGatewayLogs` resource-specific table (`ApiId`, `OperationId`, `ResponseCode`, `BackendResponseCode`, `BackendTime`, `TotalTime`, `LastErrorReason`). Consumption does not support resource logs. **Application Insights** logging has a per-API Sampling (%) setting and an "Always log errors" option.
- **APIOps** (Azure/apiops): an `extractor` pulls APIs and policies to a Git repo and a `publisher` deploys them to each environment, with per-environment configuration files.
- Self-hosted gateway (container) for on-prem/edge APIs (Developer and Premium); **workspaces** for team-isolated APIs (Basic v2, Standard v2, Premium, Premium v2).

## Gotchas
- `validate-jwt` `openid-config` is fetched and cached — a private APIM without outbound to `login.microsoftonline.com` fails every request after cache expiry.
- Policy scope order: `<base/>` placement decides whether the global policy runs before or after the API policy; omit it and you silently skip global JWT validation.
- Caching: the built-in cache can be cleared during API Management updates and is not available on Consumption; an external Redis-compatible cache avoids that and can be shared by several instances in different regions (configure it under External cache in the portal).
- Subscription keys in query strings get logged everywhere; prefer header-only; `az apim api create/import` has `--subscription-key-header-name` and `--subscription-key-query-param-name` to rename the carriers.
- Revisions are **not** versions: making a revision current changes behaviour for every consumer; versions give consumers a choice.
- Classic-tier VNet injection is limited to Developer and Premium; Standard v2 offers outbound VNet integration only and Premium v2 injects the gateway only. Pick the tier by that requirement first. Creating an internal-VNet Premium instance is a long operation (the Application Gateway tutorial quotes 30 to 40 minutes).

## Verify
- [ ] `curl -H "Ocp-Apim-Subscription-Key: <k>" https://api.example.com/orders/health` → 200; without key → 401; with an expired JWT → 401 with your message.
- [ ] 101 requests in a minute → 429; `X-RateLimit-Remaining` (from `remaining-calls-header-name`) decrements.
- [ ] Stop the backend: the breaker trips, clients get 503 for the trip duration, and the pool fails over to the secondary backend.
- [ ] APIOps publisher run from a PR updates the policy; no secrets in the repo (named values reference Key Vault).

## Checked
2026-10-27. Confirmed against Learn: API Management feature comparison, virtual network concepts, backends (circuit breaker, pools), validate-jwt, rate-limit-by-key, quota-by-key, cache-lookup, set-backend-service, forward-request, authentication-managed-identity and retry policy pages, named values and Key Vault, external cache, Azure Monitor and Application Insights logging, ApiManagementGatewayLogs column list, the az apim CLI reference (create, api import, api release create, backend create, nv create, product create, product api add) and the Azure/apiops README.
Corrected: tier matrix (VNet integration is Standard v2/Premium v2; injection is Developer/Premium/Premium v2; workspaces and self-hosted tiers), `--circuit-breaker` and `--key-vault-secret-identifier` flags that do not exist, `az apim cache` and `az apim api diagnostic` which are not in the CLI reference, provisioning times.
Removed: unconfirmed metric names, capacity threshold, `context.Deployment.Region`, per-instance cache claim, error text of the missing-key 401.
Method: documentation only; no commands were run.
