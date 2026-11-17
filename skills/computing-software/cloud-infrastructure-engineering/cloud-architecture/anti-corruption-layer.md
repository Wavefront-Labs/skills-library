---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.anti-corruption-layer
name: anti-corruption-layer
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, design-patterns-cloud, anti-corruption-layer, acl, domain-driven-design, bounded-context, legacy-integration, translation-layer, adapter, modernisation]
level: advanced
status: docs-checked
description: "Shield a new service's model from a legacy or third-party model with a translation layer: placement, mapping rules, error translation, and retiring it after migration."
sources: ["https://learn.microsoft.com/azure/architecture/patterns/anti-corruption-layer"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Anti-corruption layer

During modernisation, new services must talk to the legacy system. If they adopt its data model
(`CUST_FLG_3`, overloaded status codes), the legacy design leaks into the new system forever.

## Steps
1. **Define the new bounded context's model first** (your terms, your invariants).
2. Build the ACL as a facade or adapter layer that holds all the translation logic between the two systems. Calls
   from your system always use your model; calls to the legacy side conform to its data model or methods.
   Decide whether it handles all communication between the subsystems or only a subset of features.
3. Placement: a component within the application, or an independent service. A separate service adds latency
   and something to manage and maintain, so plan how it scales and how it fits your monitoring, release and
   configuration processes; you may need more than one ACL (for example for different technologies).
4. Translate **errors and semantics**, not just fields: legacy "status 9" may mean three things;
   map to explicit domain states or reject.
5. Validate and sanitise input at this boundary, since the two systems may have different trust levels.
   Contract-test the ACL against recorded legacy responses (team practice) so legacy changes break tests, not prod.
6. Make it observable: correlation IDs and structured logging to diagnose translation failures; track the
   success and latency of translation.
7. Plan its removal: decide up front whether it is permanent or retired once all legacy functionality has
   migrated (see strangler fig).

## Gotchas
- ACL grows into a second monolith full of business logic — keep it translation-only; avoid business rules or
  orchestration in the layer.
- It adds latency to calls and is a possible single point of failure; plan resilience (retry, circuit breaker,
  bulkhead, health endpoint monitoring) and maintain and monitor transaction and data consistency.
- An event-driven (message-based) ACL can decouple the modern domain from the legacy system's throughput limits.

## Verify
- [ ] New service code contains no legacy field names/codes (grep).
- [ ] Contract tests run in CI against captured legacy payloads.

## Checked
2026-11-08. Confirmed against the Azure Architecture Center Anti-Corruption Layer pattern page (read in full:
facade or adapter, component or independent service, latency and maintenance cost, scaling, subset of features,
permanent vs retired, input validation, observability, resilience patterns, asynchronous variant, translation only).
Removed the book citation (Evans, not a readable URL; the Azure page attributes the pattern to him) and the unsourced
facade/adapters/translators split, cache-and-batch and bidirectional-sync advice. Contract testing against captured
payloads and the "grep for legacy names" check are team practice, not vendor claims.
Method: documentation only; no commands were run.

Related: computing-software.cloud-infrastructure-engineering.cloud-architecture.strangler-fig
