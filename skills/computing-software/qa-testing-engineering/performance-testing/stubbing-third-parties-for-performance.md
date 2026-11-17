---
id: computing-software.qa-testing-engineering.performance-testing.stubbing-third-parties-for-performance
name: stubbing-third-parties-for-performance
category: computing-software
field: qa-testing-engineering
product: performance-testing
tags: [performance-stubs, third-party-stubs, latency-injecting-mocks, wiremock-performance]
level: practitioner
status: draft
description: "Replace third-party dependencies with performance stubs during load tests: realistic latency distributions, rate limits, stub capacity, and keeping one path to the real service."
sources:
  - https://wiremock.org/docs/simulating-faults/
  - https://wiremock.org/docs/standalone/docker/
  - https://github.com/Shopify/toxiproxy
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Stubbing third parties in performance environments

**Why stub:** payment gateways, SMS, maps and partner APIs often forbid load testing, charge per call, rate-limit sandboxes, or have sandbox latency unlike production. Stubs make tests repeatable and legal.

## Requirements for a good performance stub
1. **Realistic latency** with a distribution, not a constant:
```json
{ "request": { "method": "POST", "urlPath": "/v1/charges" },
  "response": { "status": 200, "jsonBody": { "id": "ch_test", "status": "succeeded" },
                "delayDistribution": { "type": "lognormal", "median": 180, "sigma": 0.4 } } }
```
(WireMock; `uniform` and `fixedDelayMilliseconds` also available.) Derive median/p99 from production APM spans to that provider.
2. **Failure modes** at production rates: timeouts, 5xx, 429 with `Retry-After`.
3. **Capacity:** the stub must outperform the system under test. Run WireMock with `--container-threads`, `--async-response-enabled`, `--no-request-journal` (journal grows memory), and monitor its CPU. Consider lighter stubs (Mountebank, a tiny Go server) for very high rates.
4. **Response variety:** templated responses so ids differ (`{{randomValue type='UUID'}}` with response templating).

## Architecture
Route via configuration (base URL env var per environment), not code flags. Keep a low-rate scenario hitting the provider's real sandbox to detect contract drift.

## What you lose
Stubs hide the real provider's behaviour under your load (their rate limits, slow days). Mitigate with contract tests and production observability on the dependency.

## Gotchas
- Zero-latency stubs make your service look faster and change thread/connection usage patterns: always add latency.
- Request journal and verbose logging in the stub become the bottleneck.

## Verify
Stub CPU stays well below saturation during peak; latency of calls to the stub, measured from the app's spans, matches the configured distribution.
