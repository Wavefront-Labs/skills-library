---
id: computing-software.ai-ml-engineering.kserve.kserve-canary-rollout
name: kserve-canary-rollout
category: computing-software
field: ai-ml-engineering
product: kserve
tags: [canary, canarytrafficpercent, rollback, knative-revision, traffic-split, latestrolledoutrevision, prevrolledoutrevision]
level: practitioner
status: docs-checked
description: "Canary rollout of an InferenceService in Knative mode with canaryTrafficPercent: traffic split between revisions, unhealthy-revision behaviour, rollback."
sources: ["https://github.com/kserve/website/blob/main/docs/model-serving/predictive-inference/rollout-strategies/canary.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Canary rollout

Supported in serverless (Knative) deployment mode only.

KServe tracks the last good revision that received 100% of traffic. Set `canaryTrafficPercent` in the component spec to the percentage of traffic the NEW revision should get; the remainder stays on the last rolled-out revision.

```yaml
spec:
  predictor:
    canaryTrafficPercent: 10
    model:
      modelFormat: {name: tensorflow}
      storageUri: "gs://bucket/models/v2"
```

Behaviour:
- The first revision gets 100% of traffic.
- With a second revision and `canaryTrafficPercent: 10`, 10% goes to the new revision and 90% to `LatestRolledoutRevision`.
- Traffic is not routed to an unhealthy or bad revision.
- When the rollout step succeeds, the `LatestReadyRevision` is promoted to `LatestRolledoutRevision` and gets 100% of traffic.
- The strategy is configurable with multiple steps and can roll back if a step fails: 100% of traffic is then pinned to the previous good revision, the `PreviousRolledoutRevision`.

## Checked
Method: docs-only read of cited pages, 2026-11-08
Confirmed against the KServe website canary.md page. Removed the advice to use rolling updates in Standard mode and the `kubectl get isvc` column list, which this page does not state.
