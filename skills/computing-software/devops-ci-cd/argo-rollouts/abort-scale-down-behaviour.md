---
id: computing-software.devops-ci-cd.argo-rollouts.abort-scale-down-behaviour
name: abort-scale-down-behaviour
category: computing-software
field: devops-ci-cd
product: argo-rollouts
tags: [abortscaledowndelayseconds, abort, scale-down, aborted-rollout, blue-green, canary, argo-rollouts]
level: advanced
status: docs-checked
description: "Control whether the new ReplicaSet is scaled down after an aborted rollout using abortScaleDownDelaySeconds."
sources:
  - https://argo-rollouts.readthedocs.io/en/stable/features/scaledown-aborted-rs/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
When an update is aborted, Argo Rollouts can scale down the new ReplicaSet for all strategies. `abortScaleDownDelaySeconds` controls this; it does not apply to v1.0. The default (nil) in v1.1 and later scales the new ReplicaSet down after 30 seconds on abort.

| Strategy | abortScaleDownDelaySeconds | Behaviour (v1.1+) |
|---|---|---|
| blue-green | nil | scales down after 30 seconds |
| blue-green | 0 | does not scale down |
| blue-green | N | scales down after N seconds |
| basic canary | n/a | rolling update back to stable |
| canary with traffic routing | nil | scales down after 30 seconds |
| canary with traffic routing | 0 | does not scale down |
| canary with traffic routing | N | scales down after N seconds |

Before v1.1, blue-green never scaled down and traffic-routed canaries scaled down immediately. The table notes that traffic-routed canary combined with `setCanaryScale` did not scale down (listed as a bug in older versions) and should now behave like plain traffic-routed canary.

```yaml
strategy:
  blueGreen:
    abortScaleDownDelaySeconds: 600
```

A larger value keeps the new ReplicaSet scaled up for longer after an abort; 0 leaves it scaled up indefinitely.

Combine with `dynamicStableScale`: dynamic scaling scales the canary down as traffic returns unless you set this delay.

Verify with `kubectl get rs` after `kubectl argo rollouts abort NAME`.

## Checked

2026-11-03. Confirmed against the Argo Rollouts documentation pages: https://argo-rollouts.readthedocs.io/en/stable/features/scaledown-aborted-rs/, https://argo-rollouts.readthedocs.io/en/stable/features/canary/.

Removed or corrected: the debugging (logs, exec) and capacity-cost commentary.

Method: documentation only; no commands were run.
