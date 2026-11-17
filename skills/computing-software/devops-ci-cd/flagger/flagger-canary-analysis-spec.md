---
id: computing-software.devops-ci-cd.flagger.flagger-canary-analysis-spec
name: flagger-canary-analysis-spec
category: computing-software
field: devops-ci-cd
product: flagger
tags: [analysis, interval, threshold, stepweight, maxweight]
level: practitioner
status: docs-checked
description: "Tune Flagger canary analysis fields interval, threshold, maxWeight, stepWeight, iterations and readiness thresholds, and compute rollout and rollback time."
sources:
  - https://raw.githubusercontent.com/fluxcd/flagger/main/docs/gitbook/usage/how-it-works.md
  - https://raw.githubusercontent.com/fluxcd/flagger/main/docs/gitbook/usage/deployment-strategies.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The `analysis` block holds: `interval` (schedule, default 60s), `threshold` (max failed checks before rollback), `maxWeight` and `stepWeight` (percent), `stepWeightPromotion`, `iterations` (A/B and blue/green), `primaryReadyThreshold` and `canaryReadyThreshold` (percent of pods that must be ready before rollout; default 100), `match`, `metrics`, `alerts` and `webhooks`. It also selects the deployment strategy.

Timing formulas for a weight-based canary:

```text
interval * (maxWeight / stepWeight)    # minimum time to validate and promote
interval * threshold                    # time to roll back when checks fail
```

For A/B and blue/green the minimum is `interval * iterations`. With `interval: 1m`, `maxWeight: 50`, `stepWeight: 2` the run takes 25 minutes. With `stepWeightPromotion` set, promotion also happens in stages, moving traffic back to the primary progressively until it reaches 100 percent.

A change to the Deployment PodSpec, or to ConfigMaps and Secrets mounted as volumes or mapped to environment variables, triggers an analysis.

## Checked

2026-11-03. Confirmed against the Flagger documentation: https://raw.githubusercontent.com/fluxcd/flagger/main/docs/gitbook/usage/how-it-works.md, https://raw.githubusercontent.com/fluxcd/flagger/main/docs/gitbook/usage/deployment-strategies.md.

No wrong claims found; nothing needed removing.

Method: documentation only; no commands were run.
