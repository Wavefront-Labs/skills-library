---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.edge-functions
name: edge-functions
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, caching-strategy, edge-functions, edge-compute, cloudfront-functions, cloudflare-workers]
level: practitioner
status: draft
description: "Use edge functions well: suitable tasks, runtime limits per platform, state and data access at the edge, deployment, testing and observability."
sources: ["https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/edge-functions.html", "https://developers.cloudflare.com/workers/platform/limits/", "https://learn.microsoft.com/azure/frontdoor/front-door-rules-engine"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Edge functions

## Platforms and limits
- **CloudFront Functions**: JavaScript, sub-ms, viewer request/response only, no network
  calls, 10 KB code. Header rewrites, redirects, cache key normalisation, simple auth token checks.
- **Lambda@Edge**: Node/Python, origin and viewer triggers, network access, higher latency
  and cost, deployed from us-east-1.
- **Cloudflare Workers**: V8 isolates, CPU-time limits per plan, KV/D1/Durable Objects for state.
- **Azure Front Door rules engine** (declarative) rather than code; Fastly Compute (Wasm).

## Good uses
Redirects and URL rewrites, A/B assignment, header security, geo-based routing, JWT
validation, image format negotiation, bot filtering, personalisation from cookies.

## Steps
1. Keep logic small and stateless; edge state stores are eventually consistent.
2. Avoid calling a single-region backend from every edge request; that erases the benefit.
3. Test locally with platform tooling (Wrangler, CloudFront Functions test API) and with
   unit tests; deploy via IaC with staged rollout.
4. Observability: logs are distributed by edge location; export to a central store; track errors and CPU time.

## Gotchas
- Lambda@Edge logs land in the region nearest each edge, not one region.
- Edge code runs on every request; a bug becomes a global outage. Canary deployments matter.

## Verify
- [ ] Edge function in IaC with tests and staged rollout.
- [ ] Error and latency metrics monitored centrally.
