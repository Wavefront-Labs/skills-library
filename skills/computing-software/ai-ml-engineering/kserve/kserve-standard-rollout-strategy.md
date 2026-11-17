---
id: computing-software.ai-ml-engineering.kserve.kserve-standard-rollout-strategy
name: kserve-standard-rollout-strategy
category: computing-software
field: ai-ml-engineering
product: kserve
tags: [deploymentstrategy, rollingupdate, maxsurge, maxunavailable, rollout-strategy, availability, resourceaware, defaultrollout, deploymentrolloutstrategy, ray-node-count]
level: practitioner
status: docs-checked
description: "Set Standard mode rollout via deploymentStrategy RollingUpdate maxSurge/maxUnavailable, ConfigMap deploy defaults, multinode override and precedence order."
sources: ["https://github.com/kserve/website/blob/main/docs/model-serving/predictive-inference/rollout-strategies/rollout-strategy-standard.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Rollout strategy (Standard mode)

Precedence, highest first:
1. Multinode override (automatic when `RAY_NODE_COUNT` is in the config): `maxUnavailable: 0%`, `maxSurge: 100%`, beats everything.
2. `deploymentStrategy` in the component spec (recommended).
3. ConfigMap default, only when `defaultDeploymentMode` is `"Standard"` and no component strategy is set.
4. KServe defaults: `maxUnavailable: 25%`, `maxSurge: 25%`.

```yaml
metadata:
  annotations: {serving.kserve.io/deploymentMode: "Standard"}
spec:
  predictor:
    deploymentStrategy:
      type: RollingUpdate
      rollingUpdate: {maxUnavailable: "0", maxSurge: "1"}
  transformer:
    deploymentStrategy:
      type: RollingUpdate
      rollingUpdate: {maxSurge: "0", maxUnavailable: "1"}
```

ConfigMap form (`inferenceservice-config`, key `deploy`):

```json
{"defaultDeploymentMode": "Standard",
 "deploymentRolloutStrategy": {"defaultRollout": {"mode": "Availability", "maxSurge": "1", "maxUnavailable": "1"}}}
```

## Modes
- `Availability` (zero downtime): `maxUnavailable: "0"`, set `maxSurge`; new pods start before old ones stop.
- `ResourceAware`: `maxSurge: "0"`, set `maxUnavailable`; old pods stop first, saving resources.

Values may be counts (`"1"`) or percentages (`"25%"`). The ConfigMap `mode` must be exactly `Availability` or `ResourceAware` (case-sensitive), and a direct `deploymentStrategy.type` must be `RollingUpdate`.

## Checked

Checked 2026-11-08 against the KServe website page rollout-strategy-standard.md, read in full: the precedence order, the 25% and 25% defaults, the multinode override (0% and 100%, triggered by RAY_NODE_COUNT), the ConfigMap deploy JSON shape, both modes, and the validation rules. Nothing removed.

Method: docs-only read of cited pages, 2026-11-08
