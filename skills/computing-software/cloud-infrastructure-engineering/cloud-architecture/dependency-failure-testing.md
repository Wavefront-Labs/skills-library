---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.dependency-failure-testing
name: dependency-failure-testing
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, resilience-testing, dependency-failure-testing, fault-injection-proxy, toxiproxy, latency-injection, dependency-chaos]
level: practitioner
status: draft
description: "Test how a service behaves when each dependency is down, slow or returning errors: latency/error injection with proxies or mesh faults, expected degradation and alerting."
sources: ["https://github.com/Shopify/toxiproxy", "https://istio.io/latest/docs/tasks/traffic-management/fault-injection/", "https://docs.aws.amazon.com/fis/latest/userguide/fis-actions-reference.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dependency failure testing

## Matrix
For each dependency (DB, cache, queue, internal API, third-party API, DNS, identity) test:
| Failure | Expected behaviour (write it down first) |
|---|---|
| Unavailable (connection refused) | Fail fast, fallback, circuit opens, clear error |
| Slow (added latency, e.g. +2 s) | Timeouts fire, no thread exhaustion, degraded response |
| Errors (5xx) | Retries bounded with backoff; breaker opens |
| Partial (one shard/replica) | Healthy shards still served |
| Wrong data / malformed | Validation rejects, no crash loop |

## Tools
- **Toxiproxy** between service and dependency in test environments (latency, bandwidth, timeout,
  reset_peer toxics).
- **Service mesh** fault injection (Istio VirtualService `fault.delay` / `fault.abort`).
- **AWS FIS** actions (network disruption, API throttle/error injection for some services),
  **Azure Chaos Studio** faults, Chaos Mesh / Litmus on Kubernetes.
- Unit/integration: WireMock fault responses.

## Steps
1. Write expected behaviour per row with the team.
2. Run in staging; automate as a test suite; then targeted production experiments with stop conditions.
3. Record gaps (missing timeouts, unbounded retries) as backlog items.

## Gotchas
- Testing only "down", never "slow" - slow is what causes cascading failures.
- Default client timeouts (often infinite or 60 s+).

## Verify
- [ ] Every critical dependency has a passing failure test for down and slow.
