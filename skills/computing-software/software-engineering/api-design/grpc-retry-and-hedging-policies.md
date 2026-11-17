---
id: computing-software.software-engineering.api-design.grpc-retry-and-hedging-policies
name: grpc-retry-and-hedging-policies
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, grpc, grpc-retry-policy, hedging, service-config, retry-throttling]
level: advanced
status: docs-checked
description: "Configure gRPC transparent retries, retryPolicy and hedgingPolicy in service config, with retry throttling and only for idempotent methods."
sources: ["https://grpc.io/docs/guides/retry/", "https://github.com/grpc/proposal/blob/master/A6-client-retries.md", "https://grpc.io/docs/guides/service-config/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# gRPC retry and hedging policies

gRPC clients retry from the **service config** (JSON, set by the client or
delivered by the name resolver, e.g. DNS), not hand-written loops.

```json
{"methodConfig": [{
   "name": [{"service": "orders.v1.OrderService", "method": "GetOrder"}],
   "timeout": "2s",
   "retryPolicy": {
     "maxAttempts": 4, "initialBackoff": "0.1s", "maxBackoff": "1s",
     "backoffMultiplier": 2, "retryableStatusCodes": ["UNAVAILABLE"]}}],
 "retryThrottling": {"maxTokens": 10, "tokenRatio": 0.1}}
```

## Rules
- Retry only idempotent methods (reads, or writes with request ids). Retry codes: usually just
  `UNAVAILABLE`; maybe `RESOURCE_EXHAUSTED` if servers set pushback. Never `INTERNAL`,
  or `INVALID_ARGUMENT`.
- `maxAttempts` must be greater than 1 and values above 5 are treated as 5 (the client-side maximum, changeable by channel argument).
- **retryThrottling** is a token bucket kept per server name: each failed RPC (retryable code or no-retry pushback) costs 1 token, each success adds
  `tokenRatio`; while tokens <= maxTokens/2 RPCs are not retried and hedged RPCs beyond the first are not sent. This is the retry budget preventing storms.
- Servers can push back: trailing metadata `grpc-retry-pushback-ms` (negative = don't retry).
- Transparent retries (request never left the client / never reached server app) happen
  automatically regardless of policy.

## Hedging
```json
"hedgingPolicy": {"maxAttempts": 3, "hedgingDelay": "0.05s", "nonFatalStatusCodes": ["UNAVAILABLE"]}
```
Sends a second copy if the first hasn't answered within `hedgingDelay`, takes the
first reply, cancels the rest. Cuts tail latency for idempotent reads at the cost of extra load.
A method has either retryPolicy or hedgingPolicy, not both.

## Verify
Check the client logs/metrics `grpc.client.attempt.*` (OpenTelemetry) show attempts; fault-inject
UNAVAILABLE at 20% and confirm success rate holds without load blowing up.

## Checked
2026-11-01. Confirmed against gRFC A6 (client retries) and the gRPC retry guide: retryPolicy and hedgingPolicy fields, maxAttempts cap of 5, per-server-name throttling with the maxTokens/2 threshold and tokenRatio, grpc-retry-pushback-ms, transparent retries, one policy per RPC, grpc.client.attempt metrics. Removed: p95 hedging-delay advice, DEADLINE_EXCEEDED reasoning, xDS delivery claim.
Method: documentation only; no commands were run.
