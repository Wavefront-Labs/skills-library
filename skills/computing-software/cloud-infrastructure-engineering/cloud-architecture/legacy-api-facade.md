---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.legacy-api-facade
name: legacy-api-facade
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, modernisation, legacy-api-facade, facade-pattern, api-wrapping, anti-corruption-layer, legacy-integration, api-management]
level: practitioner
status: draft
description: "Put a modern API facade in front of a legacy system (screen, file, SOAP or DB interfaces) to decouple consumers and enable incremental replacement behind the same contract."
sources: ["https://learn.microsoft.com/azure/architecture/patterns/anti-corruption-layer", "https://martinfowler.com/bliki/StranglerFigApplication.html", "https://learn.microsoft.com/azure/api-management/api-management-key-concepts"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# API facade over legacy systems

## Steps
1. Design the target API contract from consumer needs (resource model, errors, pagination) - not
   a 1:1 copy of the legacy interface.
2. Implement the facade service that translates: REST/JSON <-> SOAP, MQ, stored procedures, batch
   files, or (last resort) screen scraping/RPA.
3. Publish through API management for auth, throttling (protect fragile legacy capacity), caching
   of read-mostly data, and analytics.
4. Add resilience: timeouts, circuit breaker, bulkhead around the legacy backend; queue writes
   where the legacy cannot handle bursts.
5. Migrate consumers to the facade; block direct legacy access afterwards.
6. Replace functionality behind the facade incrementally (strangler), routing per operation.

## Gotchas
- Leaking legacy codes and field names through the facade; translate them.
- Facade becomes a new monolith when it accumulates business logic; keep it translation +
  orchestration only.
- Legacy throughput limits - enforce with rate limits at the gateway, measure with load tests.

## Verify
- [ ] Contract tests run against the facade.
- [ ] Legacy load stays within its tested capacity at peak consumer traffic.
