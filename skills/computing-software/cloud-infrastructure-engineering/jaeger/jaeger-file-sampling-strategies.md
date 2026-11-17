---
id: computing-software.cloud-infrastructure-engineering.jaeger.jaeger-file-sampling-strategies
name: jaeger-file-sampling-strategies
category: computing-software
field: cloud-infrastructure-engineering
product: jaeger
tags: [jaeger, sampling-strategies-json, service-strategies, default-strategy, operation-strategies]
level: practitioner
status: docs-checked
description: "Serve per-service and per-operation sampling strategies from a reloadable JSON file via the remote_sampling extension."
sources:
  - https://www.jaegertracing.io/docs/2.22/architecture/sampling/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: set central sampling rules without adaptive sampling.

```
remote_sampling:
  file:
    path: ./cmd/jaeger/sampling-strategies.json
```
The file is automatically reloaded when its contents change. With no configuration, Jaeger returns a default probabilistic policy with probability 0.001 (0.1 percent) for all services.

Example sampling-strategies.json:
```
{
  "service_strategies": [
    {"service": "foo", "type": "probabilistic", "param": 0.8,
     "operation_strategies": [
       {"operation": "op1", "type": "probabilistic", "param": 0.2},
       {"operation": "op2", "type": "probabilistic", "param": 0.4}]},
    {"service": "bar", "type": "ratelimiting", "param": 5}
  ],
  "default_strategy": {"type": "probabilistic", "param": 0.5,
    "operation_strategies": [
      {"operation": "/health", "type": "probabilistic", "param": 0.0},
      {"operation": "/metrics", "type": "probabilistic", "param": 0.0}]}
}
```
Types are `probabilistic` and `ratelimiting`; ratelimiting is not supported for `operation_strategies`. `default_strategy` is the catch-all for services not in `service_strategies`. Here foo is sampled at 0.8 except op1 and op2; bar is limited to 5 traces per second; others get 0.5; and /health and /metrics are disabled (probability 0) for every service that does not define its own strategies for them.

## Checked

2026-11-03. Confirmed against the Sampling page: file path configuration and automatic reload, the 0.001 default probabilistic policy, the example strategies file, the two types, ratelimiting not supported for operation_strategies, and default_strategy semantics. Nothing removed.
Method: documentation only; no commands were run.
