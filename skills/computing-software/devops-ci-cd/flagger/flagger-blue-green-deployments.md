---
id: computing-software.devops-ci-cd.flagger.flagger-blue-green-deployments
name: flagger-blue-green-deployments
category: computing-software
field: devops-ci-cd
product: flagger
tags: [blue-green, iterations, deployment-strategy, kubernetes-provider]
level: practitioner
status: docs-checked
description: "Run Flagger blue/green releases by replacing stepWeight and maxWeight with iterations, with or without a service mesh."
sources:
  - https://raw.githubusercontent.com/fluxcd/flagger/main/docs/gitbook/usage/deployment-strategies.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Blue/green needs no mesh or ingress controller (Kubernetes L4 networking works) and is supported for all mesh providers. Replace `stepWeight/maxWeight` with `iterations`:

```yaml
analysis:
  interval: 1m
  iterations: 10
  threshold: 2
```

Flagger runs conformance and load tests on the canary (green) pods for ten minutes. If metrics pass, live traffic is switched when the canary is promoted.

Sequence with a mesh: detect new revision, scale up canary, run conformance tests, run load tests and metric checks every minute, abort at the failure threshold, route traffic to canary (not done with the plain Kubernetes provider), promote the canary spec over the primary, wait for the primary rollout, route traffic back to primary, scale down canary. Routing to green before the primary rolling update avoids dropping in-flight requests.

## Checked

2026-11-03. Confirmed against the Flagger documentation: https://raw.githubusercontent.com/fluxcd/flagger/main/docs/gitbook/usage/deployment-strategies.md.

No wrong claims found; nothing needed removing.

Method: documentation only; no commands were run.
