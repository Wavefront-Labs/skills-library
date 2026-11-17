---
id: computing-software.devops-ci-cd.argo-rollouts.bluegreen-scale-down-and-preview-replicas
name: bluegreen-scale-down-and-preview-replicas
category: computing-software
field: devops-ci-cd
product: argo-rollouts
tags: [blue-green, scaledowndelayseconds, previewreplicacount, scaledowndelayrevisionlimit, iptables, argo-rollouts]
level: advanced
status: docs-checked
description: "Tune scaleDownDelaySeconds, previewReplicaCount and scaleDownDelayRevisionLimit for blue-green rollouts."
sources:
  - https://argo-rollouts.readthedocs.io/en/stable/features/bluegreen/
  - https://argo-rollouts.readthedocs.io/en/stable/features/specification/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Three blue-green fields control resource use and safety around the switch.

**scaleDownDelaySeconds** (default 30) delays scaling down the old ReplicaSet after the active Service moves to the new one. The docs warn that after a selector change there is a propagation delay before all nodes update iptables; during it, traffic still goes to old pods. The specification advises a minimum of 30 seconds so old pods are not killed while packets still target them.

If `postPromotionAnalysis` is configured and `scaleDownDelaySeconds` is set, the controller cancels any running AnalysisRuns when the delay elapses to scale down. If it is omitted and post analysis exists, scale-down waits for the AnalysisRun to complete (minimum 30 seconds).

**previewReplicaCount** runs fewer replicas under the preview Service while testing, saving resources. Before promotion the controller scales the new ReplicaSet to `spec.replicas`, and the active Service does not switch until it is fully available. If omitted the preview stack runs at 100%.

**scaleDownDelayRevisionLimit** caps how many old active ReplicaSets stay scaled up waiting for their delay. If omitted, all are retained for the delay.

**abortScaleDownDelaySeconds** (default 30, 0 means never) delays scaling down the preview ReplicaSet after an abort.

```yaml
blueGreen:
  scaleDownDelaySeconds: 60
  previewReplicaCount: 1
  scaleDownDelayRevisionLimit: 2
```

Verify old ReplicaSets with `kubectl get rs`.

## Checked

2026-11-03. Confirmed against the Argo Rollouts documentation pages: https://argo-rollouts.readthedocs.io/en/stable/features/bluegreen/, https://argo-rollouts.readthedocs.io/en/stable/features/specification/.

Removed or corrected: the app label selector in the verify command.

Method: documentation only; no commands were run.
