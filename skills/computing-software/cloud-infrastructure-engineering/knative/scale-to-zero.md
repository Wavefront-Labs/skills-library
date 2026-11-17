---
id: computing-software.cloud-infrastructure-engineering.knative.scale-to-zero
name: scale-to-zero
category: computing-software
field: cloud-infrastructure-engineering
product: knative
tags: [scale-to-zero, enable-scale-to-zero, scale-to-zero-grace-period, pod-retention-period]
level: practitioner
status: docs-checked
description: "Enable or disable scale to zero and tune grace period and last pod retention."
sources:
  - https://knative.dev/docs/serving/autoscaling/scale-to-zero/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: decide whether idle Revisions drop to zero pods and how gracefully.

Scale to zero requires the Knative Pod Autoscaler (KPA) and can only be enabled or disabled globally.

Settings in the `config-autoscaler` ConfigMap (namespace `knative-serving`):
- `enable-scale-to-zero`: boolean, default `true`. If `false`, Revisions stop at 1 replica. No per-revision setting.
- `scale-to-zero-grace-period`: duration, default `30s`, no per-revision annotation. It is an upper bound on how long the system waits for scale-from-zero machinery (internal network programming) to be ready before the last replica is removed. Change it only if requests drop while scaling to zero. It does not set how long the last replica lives after traffic ends and does not guarantee the replica stays that long.
- `scale-to-zero-pod-retention-period`: non-negative duration, default `0s`. Annotation `autoscaling.knative.dev/scale-to-zero-pod-retention-period`. Keeps the last pod for at least this long after the Revision is idle.

```yaml
data:
  enable-scale-to-zero: "false"
```

Operator form:

```yaml
spec:
  config:
    autoscaler:
      enable-scale-to-zero: "false"
```

## Checked

2026-11-03. Confirmed on the Knative Serving autoscaling/scale-to-zero page: enable-scale-to-zero, grace period and pod retention period keys, defaults and warnings. Removed: the closing stable-window sentence (on another page).
Method: documentation only; no commands were run.
