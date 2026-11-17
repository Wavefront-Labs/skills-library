---
id: computing-software.cloud-infrastructure-engineering.knative.gradual-rollout
name: gradual-rollout
category: computing-software
field: cloud-infrastructure-engineering
product: knative
tags: [rollout-duration, gradual-rollout, latest-revision, configuration-target]
level: advanced
status: docs-checked
description: "Shift traffic to a new Revision in steps with the rollout-duration annotation."
sources:
  - https://knative.dev/docs/serving/rolling-out-latest-revision/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: avoid sending 100 percent of traffic to a new Revision at once.

If traffic points at a Configuration target instead of a Revision target, then when a new Revision is ready all of that target's traffic shifts to it immediately. This can make the request queue too long at the queue-proxy or activator, and requests may expire or be rejected.

The `rollout-duration` parameter shifts traffic gradually. Affected Configuration targets get 1 percent of traffic first, then equal incremental steps for the rest. It works for tagged and untagged targets, on Knative Services or on Routes without a service. It is time-based and does not interact with autoscaling.

Per Service or Route annotation:

```yaml
metadata:
  annotations:
    serving.knative.dev/rollout-duration: "380s"
```

The page points to the Administration guide for the global ConfigMap setting (not fetched here).

Status: during a rollout the Route and Service `traffic` and `conditions` status are updated. A split such as 55 percent to `configurationName: config` (latest ready Revision) and 45 percent to `revisionName: config-00005` shows the intermediate state.

Multiple rollouts: if another Revision appears mid-rollout, traffic starts shifting to the newest Revision immediately, and incomplete rollouts drain from newest to oldest.

## Checked

2026-11-03. Confirmed on the Knative Serving rolling-out-latest-revision page: rollout-duration annotation, 1 percent first step, time-based note, status example and multiple rollouts. Removed: the config-network global key (page defers to the Administration guide).
Method: documentation only; no commands were run.
