---
id: computing-software.devops-ci-cd.argo-workflows.automatic-pod-restarts
name: automatic-pod-restarts
category: computing-software
field: devops-ci-cd
product: argo-workflows
tags: [failed-pod-restart, pod-restarts, node-eviction, max-restarts, pod-restarts-total]
level: advanced
status: docs-checked
description: "Enable controller-level restarts of pods that fail before the main container starts, with restartable reasons, maxRestarts and how it differs from retryStrategy."
sources: ["https://argo-workflows.readthedocs.io/en/latest/pod-restarts/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Automatic pod restarts
Infrastructure failures before your code runs (evictions, disk pressure, admission errors) can be recovered without `retryStrategy`. Enable in the controller ConfigMap:

```yaml
data:
  failedPodRestart: |
    enabled: true
    maxRestarts: 3
```
`enabled` defaults to `false`; `maxRestarts` defaults to `3` per node.

A pod is restarted only if all hold: phase is `Failed`, the main container never reached `Running`, the reason is restartable, and the restart count is under the maximum. Restartable reasons: `Evicted` (node pressure such as `DiskPressure`, `MemoryPressure`), `NodeShutdown`, `NodeAffinity` (selector no longer matches) and `UnexpectedAdmissionError`. For safety it works only on pods known never to have started; anything that might have run needs `retryStrategy`.

The controller deletes the pod, marks the node Pending and recreates it elsewhere. Monitoring: node status gets `FailedPodRestarts` and an updated message such as `Pod auto-restarting due to Evicted: The node had condition: [DiskPressure]`. Read counts with `kubectl get wf NAME -o jsonpath='{.status.nodes[*].failedPodRestarts}'`. The metric `pod_restarts_total` is labelled by reason, condition and namespace.

Versus `retryStrategy`: restarts are global and handle pre-start infrastructure failures (counter `failedPodRestarts`), while retries are per template for application failures (counter `retries`). They combine, and restarts are safe even for non-idempotent work.

## Checked
2026-11-03. Confirmed against the Argo Workflows Automatic Pod Restarts page: the config options and defaults, the four restartable reasons, the conditions for restart, monitoring fields and the metric, and the retryStrategy comparison. The page prints `failedPodRestart` as a nested map; the block-string form above is how a ConfigMap data value must be written (the page does not show it).
Method: documentation only; no commands were run.
