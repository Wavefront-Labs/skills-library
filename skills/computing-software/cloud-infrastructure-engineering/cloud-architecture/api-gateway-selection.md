---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.api-gateway-selection
name: api-gateway-selection
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, gateway-patterns, api-gateway-selection, api-gateway, azure-api-management, amazon-api-gateway, apigee, kong, envoy-gateway]
level: practitioner
status: docs-checked
description: "Select an API gateway: managed cloud gateways vs Kong/Apigee, criteria for protocols, policies, developer portal, multi-cloud, limits, latency and cost model."
sources: ["https://docs.aws.amazon.com/apigateway/latest/developerguide/limits.html", "https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-execution-service-limits-table.html", "https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-quotas.html", "https://learn.microsoft.com/azure/api-management/api-management-features", "https://cloud.google.com/apigee/docs/api-platform/get-started/what-apigee", "https://docs.konghq.com/gateway/latest/", "https://raw.githubusercontent.com/kubernetes-sigs/gateway-api/main/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# API gateway product selection

## Steps
1. **Clarify the job**: external API product with developer portal and monetisation, internal
   north-south ingress, or east-west service traffic (usually a service mesh, not a gateway).
2. **Shortlist**:
   - Amazon API Gateway (REST, HTTP and WebSocket APIs; quotas differ by type). REST API integration timeout is 50 ms
     to 29 seconds by default (Regional and private APIs can request more, which may reduce your account throttle
     quota; edge-optimized cannot); HTTP API maximum integration timeout is 30 seconds; payload is 10 MB for both.
     Account throttle default is 10,000 requests per second per Region (lower in some Regions).
   - Azure API Management: tiers Consumption, Developer, Basic, Standard, Premium and the v2 tiers (Basic v2,
     Standard v2, Premium v2). Features vary by tier: for example a developer portal is in every tier except
     Consumption, multi-region deployment only in Premium, the self-hosted gateway only in Developer and
     Premium, and the Developer tier has no SLA and is for non-production use. Check the tier table for VNet
     injection, availability zones and cache size.
   - Google Apigee: API management platform with a proxy layer for security, rate limiting, quotas and analytics;
     supports REST, gRPC, SOAP and GraphQL; includes a developer portal.
   - Kong Gateway: API gateway for hybrid and multi-cloud, extensible through plugins; deployment modes include
     traditional, hybrid and DB-less.
   - Kubernetes Gateway API (`Gateway`, `HTTPRoute`, `GRPCRoute` and others are GA at `v1`): an API specification
     implemented by several controllers, useful for portable cluster ingress.
3. **Score criteria**: protocols (REST, gRPC, GraphQL, WebSocket, streaming), auth (OIDC/JWT,
   mTLS, API keys), rate limiting and quotas, transformation, portal and API catalogue,
   multi-region/multi-cloud deployment, private networking, latency overhead, observability
   exports, policy-as-code and GitOps, SLA, hard limits, and the vendor's pricing model (see its pricing page).
4. **Proof of concept** with the two top options: realistic payloads, p99 latency added, config
   in CI, failover behaviour.
5. **Decide** with an ADR covering lock-in and exit cost.

## Gotchas
- Compare per-request and fixed-unit pricing models at your expected volume (see the vendor pricing pages).
- Hard limits (timeouts, payload size) block long-running calls or big uploads; use asynchronous patterns or
  direct paths to storage.
- A gateway per team multiplies policy drift; standardise on one product per tier.

## Verify
- [ ] Criteria matrix with weights and PoC results attached to the ADR.
- [ ] Limits checked against the largest and slowest API.

## Checked
2026-11-08. Confirmed against the Amazon API Gateway quotas pages (account, REST API and HTTP API: timeout, payload,
throttle), the Azure API Management tier feature table, the Apigee overview, the Kong Gateway docs home and the
Kubernetes Gateway API README (GA resources). Removed unsupported claims: serverless pricing, ALB alternative, XML
policies, Apigee monetisation and API Gateway for Cloud Functions, Tyk, Gravitee, KrakenD, Envoy Gateway, the
OpenTelemetry and APIOps criteria wording, the "very high volume" pricing claim and header size limits. Selection
criteria and the proof-of-concept steps are advice, not vendor claims. The Gateway API website returned an empty
page, so the project README on GitHub is cited instead.
Method: documentation only; no commands were run.
