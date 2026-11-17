---
id: computing-software.devops-ci-cd.flagger.flagger-traffic-mirroring
name: flagger-traffic-mirroring
category: computing-software
field: devops-ci-cd
product: flagger
tags: [mirroring, shadow-traffic, blue-green, idempotent]
level: advanced
status: docs-checked
description: "Mirror live traffic to the Flagger canary before shifting users, with the idempotency warning and mirror settings."
sources:
  - https://raw.githubusercontent.com/fluxcd/flagger/main/docs/gitbook/usage/deployment-strategies.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Mirroring (Istio and Gateway API) copies each request: one goes to the primary, one to the canary. The primary's response is returned; the canary's is discarded. Metrics are collected on both, and the rollout only proceeds if canary metrics are healthy.

Use mirroring only for requests that are idempotent or safe to process twice. Reads are; for writes consider what happens when a request is handled by both primary and canary.

```yaml
analysis:
  interval: 1m
  iterations: 10
  threshold: 2
  mirror: true
  mirrorWeight: 100
```

Sequence: detect revision, scale up canary from zero, wait for the HPA minimum replicas, check pod health, run acceptance tests (abort on failure), start load tests, mirror 100 percent of traffic, check success rate and duration each minute, stop mirroring after the iterations, route live traffic to the canary, promote to primary, wait for primary health, switch traffic back, scale the canary to zero and notify.

## Checked

2026-11-03. Confirmed against the Flagger documentation: https://raw.githubusercontent.com/fluxcd/flagger/main/docs/gitbook/usage/deployment-strategies.md.

No wrong claims found; nothing needed removing.

Method: documentation only; no commands were run.
